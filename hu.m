clear;
clc;
close all;

f = readmatrix("scan.csv")';
f = f';
angle = f(:, 1);
dist = f(:, 2);
x = dist .* cos(angle);
y = dist .* sin(angle);




plot(x, y, '.');
% Задать пределы осей
xlim([-1, 1]);
ylim([-1, 1]);

% Сделать масштаб одинаковым по обеим осям
axis equal;

function [matr] = rotation_matr(angle)
    matr = [cos(angle) -sin(angle); sin(angle) cos(angle)];
end
