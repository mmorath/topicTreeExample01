FROM jupyter/datascience-notebook:r-4.2.3

USER root

RUN apt-get update && \ 
    apt-get install -y libpq-dev && \
    apt-get clean && rm -rf var/lib/apt/lists/*

USER $NB_UID

#RUN conda install --quiet --yes \
#    'r-rpostgresql' \
#    'r-getpass' \
#    'r-lme4' && \
RUN conda clean --all -f -y  &&  \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
