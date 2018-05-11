clear

dataset = csvread('fixed_hltv_dataset.csv');
dataset = dataset(randperm(size(dataset,1)),:);

X = dataset(1:25000,1:41);
Xval = dataset(25001:28000,1:41);
Xtest = dataset(28001:end,1:41);

y = dataset(:, 42);
for i = 1 : size(y)
    if y(i) == 0
        y(i) = 1;
    else
        y(i) = 2;
    end
end

yval = y(25001:28000);
ytest = y(28001:end);
y = y(1:25000);

[X, mu, sigma] = featureNormalize(X, 0, 0);
Xval = featureNormalize(Xval, mu, sigma);
Xtest = featureNormalize(Xtest, mu, sigma);

input_layer_size  = 41; 
hidden_layer_size = 100;
num_labels = 2;  

%% 

fprintf('\nInitializing Neural Network Parameters ...\n')

initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels);

% Unroll parameters
initial_nn_params = [initial_Theta1(:) ; initial_Theta2(:)];

fprintf('\nTraining Neural Network... \n')

options = optimset('MaxIter', 150);

lambda = 2.1;

costFunction = @(p) nnCostFunction(p, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, X, y, lambda);

[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

% Obtain Theta1 and Theta2 back from nn_params
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

pred = predict(Theta1, Theta2, X);

fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == y)) * 100);

pred = predict(Theta1, Theta2, Xval);

fprintf('\nCV Set Accuracy: %f\n', mean(double(pred == yval)) * 100);

pred = predict(Theta1, Theta2, Xtest);

fprintf('\nTest Set Accuracy: %f\n', mean(double(pred == ytest)) * 100);
             
%%

set_size = [1 50 100 200 300 1000 1600 3000 6000 15000 25000];

lambda = 2.3;

[accuracy_train, accuracy_val] = ...
    learningCurve(X, y, Xval, yval, lambda, set_size, hidden_layer_size);
plot(set_size, accuracy_train, set_size, accuracy_val);

title(sprintf('NN Learning Curve (lambda = %f)', lambda));
xlabel('Number of training examples')
ylabel('Accuracy')
axis([0 25000 0 100])
legend('Train', 'Cross Validation')


%%
lambda_vec = [0 0.01 0.1 1 2 3 10 20 30];

[lambda_vec, error_train, error_val] = ...
    validationCurve(X, y, Xval, yval, lambda_vec, hidden_layer_size);

close all;
plot(lambda_vec, error_train, lambda_vec, error_val);
legend('Train', 'Cross Validation');
xlabel('lambda');
ylabel('Error');

fprintf('lambda\t\tTrain Error\tValidation Error\n');
for i = 1:length(lambda_vec)
	fprintf(' %f\t%f\t%f\n', ...
            lambda_vec(i), error_train(i), error_val(i));
end

%%
lambda_vec = [1.5 2.1 2.2 2.3 2.4 2.5];

[min_lambda] = ...
    optimizeLambda(X, y, Xval, yval, lambda_vec, hidden_layer_size);
