function flist = cleanDir(temp)

isdir = nan(1,numel(temp));
for id1 =1 :numel(temp)
        if ~strcmp(temp(id1).name(1), '.')
                isdir(id1) = 1;
        end
end
flist = temp(find(~isnan(isdir)));

return
