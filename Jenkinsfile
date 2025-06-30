pipeline {
    agent any

    stages {
        stage('Trigger 01_CI') {
            steps {
                echo 'Starting CI job...'
                // Запускаем job 01_CI и ждём её завершения
                build job: '01_CI', wait: true, propagate: true
            }
        }

        stage('Trigger 02_CD') {
            steps {
                echo 'CI passed, starting CD job...'
                // Запускаем job 02_CD и ждём её завершения
                build job: '02_CD', wait: true, propagate: true
            }
        }
    }

    post {
        success {
            echo 'Master pipeline completed successfully!'
        }
        failure {
            echo 'Something failed in CI or CD.'
        }
    }
}