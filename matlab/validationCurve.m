function [lambda_vec, error_train, error_val] = ...
    validationCurve(X, y, Xval, yval, lambda_vec, hidden_layer_size)

input_layer_size  = 41; 
num_labels = 2;   


error_train = zeros(length(lambda_vec), 1);
error_val = zeros(length(lambda_vec), 1);



for i = 1:length(lambda_vec)
    lambda = lambda_vec(i)
    nn_params = trainNN(X, y, lambda, hidden_layer_size);
    error_train(i) = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, X, y, 0);
    error_val(i) = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, Xval, yval, 0);

end
