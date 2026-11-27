pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    parameters {
        string(name: 'WORKERS', defaultValue: '4', description: 'Потоки pytest-xdist')
        string(name: 'MARKER',  defaultValue: '',  description: 'Маркер pytest. Пусто = все тесты')
        string(name: 'RERUNS',  defaultValue: '1', description: 'Перезапуски упавших тестов')
    }

    environment {
        API_URL  = 'http://127.0.0.1:5050'
        HEADLESS = '1'
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''#!/bin/bash
                    set -e
                    . .venv/bin/activate

                    python sut/server.py --port 5050 > sut.log 2>&1 &
                    SUT_PID=$!
                    trap 'kill $SUT_PID 2>/dev/null || true' EXIT

                    for i in $(seq 1 30); do
                        curl -sf http://127.0.0.1:5050/health && break
                        sleep 1
                    done
                    curl -sf http://127.0.0.1:5050/health > /dev/null

                    pytest ${MARKER:+-m "$MARKER"} -n "$WORKERS" --reruns "$RERUNS" --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false, results: [[path: 'allure-results']]
            archiveArtifacts artifacts: 'allure-results/**, sut.log', allowEmptyArchive: true
        }
    }
}
