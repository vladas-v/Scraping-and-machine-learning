function [J, grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)

Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));


m = size(X, 1);


J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));



eye_matrix = eye(num_labels);
y_matrix = eye_matrix(y,:);

a1 = [ones(m, 1) X];
z2 = a1 * Theta1';
a2 = sigmoid(z2);
a2 = [ones(size(a2, 1), 1) a2];
z3 = a2 * Theta2';
a3 = sigmoid(z3);

log1 = ((-y_matrix) .* (log(a3)));
log2 = ((1 - y_matrix) .* (log(1 - a3)));
S = sum(sum(log1 - log2));
J = S / m;

S_Theta1 = sum(sum(Theta1(:, 2:end).^2));
S_Theta2 = sum(sum(Theta2(:, 2:end).^2));
 
reg = (lambda / (2 * m)) * (S_Theta1 + S_Theta2);
J = J + reg;

delta3 = a3 - y_matrix;

delta2 = (delta3 * Theta2(:,2:end)) .* sigmoidGradient(z2);

D1 = delta2' * a1;
D2 = delta3' * a2;

Theta1(:,1) = 0;
Theta2(:,1) = 0;

reg1 = (lambda / m) * Theta1;
reg2 = (lambda / m) * Theta2;

Theta1_grad = D1/m + reg1;
Theta2_grad = D2/m + reg2;


grad = [Theta1_grad(:) ; Theta2_grad(:)];


end
