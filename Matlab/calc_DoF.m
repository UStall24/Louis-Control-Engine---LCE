% Define thruster configuration (position [x,y,z] and direction [dx,dy,dz])
% 6 thrusters placed and oriented in mm from center of gravity without
% gripper

%% Setup Variables
% Center of Gravity position
zG = [0 0.0169 0.08698] .* 1000;

% x is forward where the Gripper is
% y is sideways
% z is up and down 
rvm = 135; % Radius Vertical Motor
rhm = 165; % Radius Horizontal Motor

deg2rad = @(x) x * pi / 180;

%% Setup B-Matrix
thruster_pos = [
     rvm*cos(deg2rad(30))  rvm*sin(deg2rad(30))  210;   % VM1 1
    -rvm*cos(deg2rad(30))  rvm*sin(deg2rad(30))  210;   % VM2 2
     0                    -rvm                 210;   % VM3 3
     0                     rhm                 180;   % HM1 4
    -rhm*cos(deg2rad(30)) -rhm*sin(deg2rad(30)) 180;   % HM2 5
     rhm*cos(deg2rad(30)) -rhm*sin(deg2rad(30)) 180    % HM3 6
];

% Centrer toutes les positions autour du centre de gravité
thruster_pos = thruster_pos - zG;  % soustraction composante par composante


thruster_dir = [ 0  0  1;   % T1
                 0  0  1;   % T2
                 0  0  1;   % T3
                 -1  0  0;   % T4
                 cos(deg2rad(60)) -sin(deg2rad(60))  0;   % T5
                 cos(deg2rad(60))  sin(deg2rad(60))  0];  % T6

n_thrusters = size(thruster_pos, 1);
B = zeros(6, n_thrusters);  % Allocation matrix

% Build allocation matrix B
for i = 1:n_thrusters
    d = thruster_dir(i, :)';     % Direction vector
    r = thruster_pos(i, :)';     % Position vector
    B(1:3, i) = d;                % Force contribution
    B(4:6, i) = cross(r, d);      % Torque contribution
end

%% Calculate thruster outputs for each DoF
labels = {'Surge (X)', 'Sway (Y)', 'Heave (Z)', 'Roll (Mx)', 'Pitch (My)', 'Yaw (Mz)'};

T_result = zeros(6, 6);
for i = 1:6
    disp(['--- ' labels{i} ' ---']);
    
    D = zeros(6,1);  % desired movement vector
    D(i) = 1;        % 1 in the desired DoF
    
    T = pinv(B) * D; % solve for thruster efforts
    T = T ./ max(abs(T));  % Normalize
    T = round(T, 2);             % round to 2 decimal places
    T_result(i, :) = T';        % Store each row (thruster outputs for a DoF)
end

%% Print Values:
for i = 1:6
    disp(['Thruster Outputs (T1 to T6):']);
    disp(T_result(i, :));
end

%% Create JSON output from thruster efforts

% Rewind and compute T for each DoF
thruster_labels = {'VM1', 'VM2', 'VM3', 'HM1', 'HM2', 'HM3'};
dof_keys = {'X_Axis', 'Y_Axis', 'Z_Axis', 'X_Axis', 'Y_Axis', 'Z_Axis'};
sections = {'Translation', 'Translation', 'Translation', 'Rotation', 'Rotation', 'Rotation'};

json_struct = struct('Translation', struct(), 'Rotation', struct());

for i = 1:6
    % Assign thruster values to struct
    entry = struct();
    for j = 1:6
        entry.(thruster_labels{j}) = T_result(i, j); % Access the i-th row (DoF) and j-th thruster
    end

    sec = sections{i};
    axis = dof_keys{i};
    json_struct.(sec).(axis) = entry;
end

% Encode to JSON and write to file
json_text = jsonencode(json_struct, 'PrettyPrint', true);
fid = fopen('thruster_outputs.json', 'w');
fwrite(fid, json_text, 'char');
fclose(fid);

disp('JSON file "thruster_outputs.json" has been created.');
