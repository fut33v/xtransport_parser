module.exports = function(grunt) {
  grunt.initConfig({ 
    coffee: {
      glob_to_multiple: {
        expand: true,
        flatten: true,
        cwd: 'app/coffee/',
        src: ['*.coffee'],
        dest: 'app/js/',
        ext: '.js'
      }
    },
    watch: {
      scripts: {
        files: ['app/coffee/*.coffee'],
        tasks: ['coffee'],
        options: {
          spawn: false
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-coffee'); 
  grunt.loadNpmTasks('grunt-contrib-watch');
}
