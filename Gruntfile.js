module.exports = function(grunt) {
    grunt.initConfig({
        scp: {
            options: {
                host: 'pi-spy-1.local',
                username: 'pi',
                password: 'raspberry'
            },
            your_target: {
                files: [{
                    cwd: 'lib',
                    src: '**/*',
                    filter: 'isFile',
                    dest: '/home/pi/projects/pi-spy/lib'
                }]
            }
        }
    });

    grunt.loadNpmTasks('grunt-scp');

    grunt.registerTask('copy', ['scp']);
};
