pipeline {
    agent any

    stages {
        stage('Build & Test') {
            steps {
                node(label: 'docker'){
                    script {
                        try {
                            checkout scm
                            withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'emrt-necd-expert', usernameVariable: 'EXPERT_USER', passwordVariable: 'EXPERT_PASSWORD'],[$class: 'UsernamePasswordMultiBinding', credentialsId: 'emrt-necd-reviewer', usernameVariable: 'REVIEWER_USER', passwordVariable: 'REVIEWER_PASSWORD'],[$class: 'UsernamePasswordMultiBinding', credentialsId: 'emrt-necd-authority', usernameVariable: 'AUTHORITY_USER', passwordVariable: 'AUTHORITY_PASSWORD']]) {
                                sh "docker-compose up -d plone"
                                sh "docker-compose up selenium"
                            }
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
