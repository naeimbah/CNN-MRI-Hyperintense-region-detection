% convert the images in imdir to nifti and save them in output. 

imdir = ...;
output = ...; 


if ~exist(output); unix(sprintf('mkdir %s', output)); end;
temp = dir(sprintf('%s/', imdir));

% remove . and .. 
flist = cleanDir(temp);

for id1 = 1%:numel(flist);
	pid = flist(id1).name;
	fprintf('%s - %s : Processing %i of %i : %s\n', datestr(now), mfilename, id1, numel(flist), pid);
	dir1 = cleanDir(dir(sprintf('%s/%s', imdir, pid)));
	for id2 = 1:numel(dir1)
		dir1name = dir1(id2).name;
		dir2 = cleanDir(dir(sprintf('%s/%s/%s', imdir, pid, dir1name)));
		for id3 = 1:numel(dir2)
			dir2name = dir2(id3).name;
			dir3 = cleanDir(dir(sprintf('%s/%s/%s/%s', imdir, pid, dir1name, dir2name)));
			dcminfo = dicominfo(sprintf('%s/%s/%s/%s/%s', imdir, pid, dir1name, dir2name, dir3(1).name));
			unix(sprintf('mri_convert %s/%s/%s/%s/%s %s/%s_%s.nii', imdir, pid, dir1name, dir2name, dir3(1).name, output, pid, dcminfo.StudyDate));
			clear dir2name dir3 dcminfo
		end
		clear dir1name dir2
	end
	clear pid dir1 
end
	

