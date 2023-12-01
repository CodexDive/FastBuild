FROM 10.101.12.128/project/fastbuild_base_image:1.0
MAINTAINER MEI
SHELL ["/bin/bash", "-c"]
WORKDIR /home/fastbuild/
COPY Fastbuild.sh /home/fastbuild/Fastbuild
ENTRYPOINT [ "/bin/bash", "-c", "python /home/fastbuild/Fastbuild/main.py" ]
