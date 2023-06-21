%Script for pitch controller
% Longitudinal

% Constants
g = 9.81;  % [m/s^2]
rho = 1.225;  % [kg/m^3]
S = 0.76;
b = 3;
V = 15.1;
Sh = 0.123708;
lh = 1.03;
dclddc = 0.22;
CNw = 0.82;
CNh0 = 0.2835;

% Aircraft parameters
mac = 0.25333;  % [m]
V_0 = 15.1;  % [m/s]
mass = 8.86;  % [kg] preliminary
W = mass * g;
I_xx = 3.16189;
I_yy = 0.97871;
I_zz = 5.90325;

% Stability derivatives
mu_b = mass * g / b;
muc = mass * g / mac;

% find K
K_xx = I_xx / (rho * S * mac^3 * mu_b);
K_yy = I_yy / (rho * S * mac^3 * muc);
K_zz = I_zz / (rho * S * mac^3 * mu_b);
K_xz = 0;  % placeholder

% Row 1
C_X_u = 0.0001311;  
C_X_a = -0.5742598;  
C_Z_0 = 0.7764510;  
C_X_q = 0.4557234;  

% Row 2
C_Z_u = 0.0021766;  
C_Z_a = 5.644108;  
C_Z_a_dot = 0;  
C_X_0 = 0.0399138;  
C_Z_q = 9.9805365;  

% Row 4
C_m_u = 0.0010981;  
C_m_a = -0.8632242;  
C_m_a_dot = 0;  
C_m_q = -32.7477863;  

% Control derivatives
C_X_dc_u = 0;
C_X_dc_l = 0;
C_Z_dc_u = 0.03581;
C_Z_dc_l = -0.03581;
C_m_dc_u = 0.1456;
C_m_dc_l = -0.1456;

% PQR form
P_long = [-2 * muc * mac / V_0, 0, 0, 0;
          0, (C_Z_a_dot - 2 * muc) * mac / V_0, 0, 0;
          0, 0, -mac / V_0, 0;
          0, C_m_a_dot * mac / V_0, 0, -2 * muc * K_yy * mac / V_0];

Q_long = [-C_X_u, -C_X_a, -C_Z_0, 0;
          -C_Z_u, -C_Z_a, -C_X_0, -C_Z_q - 2 * muc;
          0, 0, 0, -1;
          -C_m_u, -C_m_a, 0, -C_m_q];

R_long = [-C_X_dc_u -C_X_dc_l;
          -C_Z_dc_u -C_Z_dc_l;
          0 0;
          -C_m_dc_u -C_m_dc_l];

% State Space Matrices
A_long = inv(P_long) * Q_long
B_long = inv(P_long) * R_long
C_long = eye(4)
D_long = zeros(4,2)

