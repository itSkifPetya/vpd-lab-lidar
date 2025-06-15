
close all;


figure;
title("Облака точек после грубого смещения")
hold on; grid on;
f1 = readmatrix("square.csv", "NumHeaderLines", 1);
x = f1(:, 1);
y = f1(:, 2);
M = [x y];
plot(x, y, '.', 'DisplayName' ,"M");
[x, y] = dots_offset(f1, 0.05, 0.064, -0.01*pi/180);
S = [x y];
% x = f2(:, 1);
% y = f2(:, 2);
plot(x, y, '.', 'DisplayName', 'S');
legend('show', 'Location', 'bestoutside')
hold off;
euclid_dist([2;0], [0;2])







% figure; hold on; grid on;
% dfplot("square.csv", 0, 0, 1)
% % figure; hold on; grid on;
% dfplot("square.csv", 3, 2, rotation_matr(pi/4))


% rotation_matr(pi/2)

function dfplot(str, t_x, t_y, r_matr)
    f = readmatrix(str, "NumHeaderLines", 1);
    % f = r_matr*f';
    x = f(1, :) + t_x;
    y = f(2, :) + t_y;
    plot(x, y, '.');

end


function [x, y] = dots_offset(f, t_x, t_y, angle)
    r_matr = rotation_matr(angle);
    f = r_matr*f';
    x = f(1, :)' + t_x;
    y = f(2, :)' + t_y;
end

function [matr] = rotation_matr(angle)
    matr = [cos(angle) -sin(angle); sin(angle) cos(angle)];
end

function [dist] = euclid_dist(s, m)
    dist = 0;
    disp(size(s));
    if  size(s) == size(m)
        for i=1:size(s)
            dist = dist + (s(i, 1) - m(i, 1))^2;
        end
        dist = sqrt(dist);
    end
end