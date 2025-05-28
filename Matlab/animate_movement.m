close all;
clear all;

%% Reading thruster_outputs
json_text = fileread('thruster_outputs.json');
data = jsondecode(json_text);

%% Defining ROV Model
% ROV dimensions
rov_size = [0.3 0.3 0.3];  % X, Y, Z in meters

% Create patch vertices and faces
[x, y, z] = ndgrid([-1 1], [-1 1], [-1 1]);
verts = [x(:), y(:), z(:)] .* rov_size / 2;

faces = [1 3 7 5;
         2 4 8 6;
         1 2 6 5;
         3 4 8 7;
         1 2 4 3;
         5 6 8 7];
% ROV dimensions
rov_size = [0.3 0.2 0.1];  % X, Y, Z in meters

% Create patch vertices and faces
[x, y, z] = ndgrid([-1 1], [-1 1], [-1 1]);
verts = [x(:), y(:), z(:)] .* rov_size / 2;

faces = [1 3 7 5;
         2 4 8 6;
         1 2 6 5;
         3 4 8 7;
         1 2 4 3;
         5 6 8 7];

%% Setup fig
figure;
axis equal;
axis([-2 2 -2 2 -2 2]);
xlabel('X'); ylabel('Y'); zlabel('Z');
view(3);
grid on;
% 
% % Plot water (blue plane)
% fill3([-2 2 2 -2], [-2 -2 2 2], [0 0 0 0], [0.4 0.6 1], 'FaceAlpha', 0.3);

% Draw ROV
rov_patch = patch('Vertices', verts, 'Faces', faces, ...
    'FaceColor', 'r', 'FaceAlpha', 0.8);


%% Simulate Physics
% Map outputs to 6-DOF movement vector
move = zeros(6,1);
fields = fieldnames(data.Translation);
for i = 1:3
    axis_name = fields{i};
    thrusts = struct2array(data.Translation.(axis_name));
    move(i) = sum(thrusts);
end
fields = fieldnames(data.Rotation);
for i = 1:3
    axis_name = fields{i};
    thrusts = struct2array(data.Rotation.(axis_name));
    move(3+i) = sum(thrusts);
end

% Normalize motion (for animation scale)
move = move / max(abs(move));

% Select movement direction
desired_dof = [1; 0; 0; 0; 0; 0];
move = desired_dof .* move;       % Apply mask


% Simulate
pos = [0; 0; 0];  % Initial position
rot = eye(3);     % Initial rotation matrix

for t = 1:100
    % Small translation and rotation per frame
    d_pos = move(1:3) * 0.01;
    d_ang = move(4:6) * 0.01;

    % Simple rotation update (approximate small angles)
    Rx = [1 0 0; 0 cos(d_ang(1)) -sin(d_ang(1)); 0 sin(d_ang(1)) cos(d_ang(1))];
    Ry = [cos(d_ang(2)) 0 sin(d_ang(2)); 0 1 0; -sin(d_ang(2)) 0 cos(d_ang(2))];
    Rz = [cos(d_ang(3)) -sin(d_ang(3)) 0; sin(d_ang(3)) cos(d_ang(3)) 0; 0 0 1];

    d_rot = Rz * Ry * Rx;
    rot = rot * d_rot;
    pos = pos + rot * d_pos;

    % Apply transform to ROV
    transformed = (rot * verts')' + pos';

    % Update plot
    set(rov_patch, 'Vertices', transformed);
    drawnow;
    pause(0.03);
end
