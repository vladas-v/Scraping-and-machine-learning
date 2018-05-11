function [accuracy_train, accuracy_val] = ...
    learningCurve(X, y, Xval, yval, lambda, set_size, hidden_layer_size)

input_layer_size  = 41; 
num_labels = 2;   

m = size(X, 1);


for index = 1 : length(set_size)
    i = set_size(index)
    nn_params = trainNN(X(1:i,:), y(1:i), lambda, hidden_layer_size);
    Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));
    Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));
    pred = predict(Theta1, Theta2, X(1:i,:));
    accuracy_train(index) = mean(double(pred == y(1:i))) * 100;
    pred = predict(Theta1, Theta2, Xval);
    accuracy_val(index) = mean(double(pred == yval)) * 100;



end
