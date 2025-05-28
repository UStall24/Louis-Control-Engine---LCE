% Définir les blocs : [x y z L W H masse]
% in Meters and KG
blocks = [
    0  0  0         0.15 0.15 0.015  1.87;   % Gewichtsplatte
    0  0  0.015     0.365 0.365 0.12  2.45;   % Untere Box
    0  0  0.135     0.365 0.365 0.12  6.75; % Obere Box
    0  0  0.255     0.365 0.365 0.14  0.2; % Buoancy 
    0  0.19  0.07   0.08 0.400 0.046  1.1; % Greifer
];

n = size(blocks, 1);
total_mass = 0;
r_cg = [0; 0; 0];

for i = 1:n
    m = blocks(i,7);
    r = blocks(i,1:3)';
    total_mass = total_mass + m;
    r_cg = r_cg + m * r;
end

r_cg = r_cg / total_mass;
disp(['Centre de gravité : ', mat2str(r_cg', 4)]);
