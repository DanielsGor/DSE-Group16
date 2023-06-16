% Description: First draft (David-Thomas) code for loading the raw data
% files from the 50N balance (Ming). Initial post-processing steps applied
% as well


function HighLiftTest_PostProcessFile()
    
    current_dir = pwd;
    % Call the HighLiftTest_PostProcessFile function with the directory path as an argument
    directory = fullfile(current_dir, 'data');
    run_post_processing(directory);
end

function run_post_processing(directory)
    % Get a list of all files in the directory
    files = dir(fullfile(directory, '*.tdms'));

    % Create a cell array to store the results
    results = cell(numel(files), 3);
    results{1, 1} = 'File Name';
    results{1, 2} = 'Mean Norm';
    results{1, 3} = 'Mean Ax';

    % Process each file
    for i = 1:numel(files)
        file = fullfile(directory, files(i).name);
        [~, file_name, ~] = fileparts(file);
        
        % Call the matlab_conversion function
        [ConvertedData,ConvertVer,ChanNames]=convertTDMS(false,file);
        rotor.time = ConvertedData.Data.MeasuredData(3).Data; % time column
        rotor.ch1 = ConvertedData.Data.MeasuredData(4).Data; % Ch1 force (Lift 1)
        rotor.ch2 = ConvertedData.Data.MeasuredData(5).Data; % Ch2 force (Lift 2) 
        rotor.ch3 = ConvertedData.Data.MeasuredData(6).Data; % Ch3 force (Lift 3)
        
        %% Processing of the data 
        % Process data
        channel1 = rotor.ch1;%-noise_wind_ch1; % Here I took noise measurments but we can zero the balance instead 
        channel2 = rotor.ch2;%-noise_wind_ch2;
        channel3 = rotor.ch3;%-noise_wind_ch3;
        
        
        total_norm = channel1 + channel2;
        total_ax = channel3;
        
        % Implement If statement for mirroring normal force
        mean_norm = mean(total_norm);
        mean_ax = mean(total_ax);

        disp(mean_norm)
        disp(mean_ax)
        % Store the results in the cell array
        results{i+1, 1} = file_name;
        results{i+1, 2} = mean_norm;
        results{i+1, 3} = mean_ax;
    end

    % Save the results to an Excel file
    output_dir = pwd;
    
    output_file = fullfile(output_dir, 'wind_tunnel_measurement_data.xlsx');
    writecell(results, output_file);
    
end


%% Inset airfoil specific data
% S = 0.201*0.4;  % Surface area model
% ws = 6;      % Flow velocity
% aoa = 0;       % Angle of attack

%% Load the datafile 
% Convert the load data
% file_folder = "C:\Users\louis\PycharmProjects\SVV\B50\DSE-Group16\Stability\wind_tunnel_test\sample_data\SampleData"; % full path to folder of file 
% file_name = "M_10_setup5_aoa_0_U_6_060623.tdms"; % file name (should end in .tdms) 
% force_file = fullfile(file_folder,file_name); % combined for the full file name
% % Read TDMS file (using function attached)
% [ConvertedData,ConvertVer,ChanNames]=convertTDMS(false,force_file);
% rotor.time = ConvertedData.Data.MeasuredData(3).Data; % time column
% rotor.ch1 = ConvertedData.Data.MeasuredData(4).Data; % Ch1 force (Lift 1)
% rotor.ch2 = ConvertedData.Data.MeasuredData(5).Data; % Ch2 force (Lift 2) 
% rotor.ch3 = ConvertedData.Data.MeasuredData(6).Data; % Ch3 force (Lift 3)
% 
% %% Processing of the data 
% % Process data
% channel1 = rotor.ch1;%-noise_wind_ch1; % Here I took noise measurments but we can zero the balance instead 
% channel2 = rotor.ch2;%-noise_wind_ch2;
% channel3 = rotor.ch3;%-noise_wind_ch3;
% 
% 
% total_norm = channel1 + channel2;
% total_ax = channel3;
% 
% % Implement If statement for mirroring normal force
% mean_norm = mean(total_norm);
% mean_ax = mean(total_ax);

% get maximum, minimum and standard deviation of normal and axial force
% min_norm = min(total_norm);
% max_norm = max(total_norm);
% std_norm = std(total_norm);
% 
% min_ax = min(total_ax);
% max_ax = max(total_ax);
% std_ax = std(total_ax);
% 
% % Convert normal and axial force to lift and drag
% mean_lift = mean_norm*cos(deg2rad(aoa)) - mean_ax*sin(deg2rad(aoa));
% mean_drag = mean_norm*sin(deg2rad(aoa)) + mean_ax*cos(deg2rad(aoa));
% % Compute cl and cd
% mean_cl = mean_lift/((1/2)*1.225*(ws^2)*(S));
% mean_cd = mean_drag/((1/2)*1.225*(ws^2)*(S));