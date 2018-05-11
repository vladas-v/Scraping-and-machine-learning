function [min_lambda] = ...
    optimizeLambda(X, y, Xtest, ytest, lambda_vec, hidden_layer_size)

input_layer_size  = 41;
num_labels = 2;   

min_lambda = 99999;
last_accuracy = 0;

for i = 1:length(lambda_vec)
    lambda = lambda_vec(i);
    nn_params = trainNN(X, y, lambda, hidden_layer_size);
    Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));
    Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));
    pred = predict(Theta1, Theta2, Xtest);
    accuracy = mean(double(pred == ytest)) * 100;
    if accuracy > last_accuracy
        min_lambda = lambda
        last_accuracy = accuracy
    end
end
end
