var gulp  = require('gulp'),
	watch = require('./semantic/tasks/watch'), 
	build = require('./semantic/tasks/build');

// import task with a custom task name
gulp.task('watch', watch);
gulp.task('build', build);

gulp.task('default', function (){
	gulp.start('watch');
});
