pipeline {
    agent any

    stages {
        stage('Build & Test') {
            steps {
                node(label: 'docker'){
                    script {
                        try {
                            checkout scm
                            sh "docker-compose up -d plone"
                            sh "docker compose up selenium"
                        }
                        finally {
                            sh "docker-compose down -v --rmi all"
                        }
                    }
                }
            }
        }
    }
}
