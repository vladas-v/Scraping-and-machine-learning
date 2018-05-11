function [nn_params] = trainNN(X, y, lambda, hidden_layer_size)

input_layer_size  = 41; 
num_labels = 2;   

initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels);


initial_nn_params = [initial_Theta1(:) ; initial_Theta2(:)];


costFunction = @(p) nnCostFunction(p, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, X, y, lambda);


options = optimset('MaxIter', 30);

[nn_params] = fmincg(costFunction, initial_nn_params, options);

end
