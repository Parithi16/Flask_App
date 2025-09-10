FROM jenkins/jenkins:lts

# Switch to root to install packages
USER root

# Install dependencies (curl, apt-utils, lsb-release, etc.)
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    sudo \
    && rm -rf /var/lib/apt/lists/*



# Install Docker CLI (uses host Docker daemon)
RUN apt-get update && \
    apt-get install -y docker.io && \
    groupadd -g 999 docker || true && \
    usermod -aG docker jenkins

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

# Install Google Cloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" \
    | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - \
    && apt-get update && apt-get install -y google-cloud-sdk \
    && rm -rf /var/lib/apt/lists/*

# Allow Jenkins user to access Docker socket
ARG DOCKER_GID=999
RUN groupmod -g ${DOCKER_GID} docker || groupadd -g ${DOCKER_GID} docker \
    && usermod -aG docker jenkins


# Switch back to Jenkins user
USER jenkins

# Expose Jenkins ports
EXPOSE 8080 50000

# Default Jenkins entrypoint
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/jenkins.sh"]
