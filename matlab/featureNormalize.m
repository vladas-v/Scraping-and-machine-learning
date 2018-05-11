function [X_norm, mu, sigma] = featureNormalize(X, mu, sigma)

if mu == 0 & sigma == 0
    mu = mean(X);
    X_norm = bsxfun(@minus, X, mu);
    
    sigma = std(X_norm);
    X_norm = bsxfun(@rdivide, X_norm, sigma);    
else
    X_norm = bsxfun(@minus, X, mu);
    X_norm = bsxfun(@rdivide, X_norm, sigma);      
end

end
