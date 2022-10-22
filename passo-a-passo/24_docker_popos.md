# Django Experience #24 - Instalando Docker no Pop!_OS

<a href="https://youtu.be/H0RS7bVymw0">
    <img src="../img/youtube.png">
</a>


# Installation of the Docker through the repository in Pop!_OS

```
sudo apt update
sudo apt install  ca-certificates  curl  gnupg  lsb-release
```


Download the GPG key of the Docker from its website and add it to the repository of Pop!_OS:

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```


Add the stable repository of the dockers from its website to the repository of Pop!_OS:

```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```


Update again

```
sudo apt update
```


Install the latest version of Dockers on Pop!_OS:

```
sudo apt install docker-ce docker-ce-cli containerd.io -y
```


After the complete installation of the Docker, we will check its status using the command:

```
sudo systemctl status docker
```


See the docker version

```
docker --version
```


Install docker-compose

```
sudo apt install docker-compose -y
```


See the docker-compose version

```
docker-compose --version
```

Ref: https://linuxhint.com/install-docker-on-pop_os/

Add group permissions

```
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo setfacl -m user:$USER:rw /var/run/docker.sock
```

Test a container example

```
docker run hello-world
```
