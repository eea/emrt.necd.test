pipeline {
    agent any

    stages {
        stage('Build & Test') {
            steps {
                node(label: 'docker'){
                    script {
                        try {
                            checkout scm
                            sh "docker build -t ${BUILD_TAG} ."
                        }
                        finally {
                            sh "docker rmi ${BUILD_TAG}"
                        }
                    }
                }
            }
        }
    }
}
