clear all
close all

%% Constants and Geometry
rV = 135; % Radius of V-Thruster to G
rH = 165; % Radius of H-Thruster to G

zG = 120;
zH = 210 - zG;
zV = 180 - zG;

a = 60 * pi / 180;
b = 30 * pi / 180;

%% B Matrix
B = [ 0,   0,   0, -cos(a), -cos(a),     1;
      0,   0,   0,  cos(b), -cos(b),     0;
      1,   1,   1,       0,       0,     0;
    -rV, rV*cos(a), rV*cos(a),  zH, -zH, 0;
      0, rV*cos(b), -rV*cos(b), zH,  zH, zH;
      0,       0,       0, rH*(cos(a)^2 + cos(b)^2), rH*(cos(a)^2 + cos(b)^2), rH ];

%% Calculate thruster outputs for each DoF
labels = {'Surge (X)', 'Sway (Y)', 'Heave (Z)', 'Roll (Mx)', 'Pitch (My)', 'Yaw (Mz)'};

for i = 1:6
    disp(['--- ' labels{i} ' ---']);
    
    D = zeros(6,1);  % desired movement vector
    D(i) = 1;        % 1 in the desired DoF
    
    T = pinv(B) * D; % solve for thruster efforts
    T = T ./ max(abs(T));
    
    disp(['Thruster Outputs (T1 to T6):']);
    disp(T');
    disp(' ');
end
