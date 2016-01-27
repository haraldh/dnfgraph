Make sure, you don't have `python3-pydot` installed, but `pydot` (maybe from F23) and `python3-pydotplus`.

Needs `python3-networkx`.


Install the modified repoquery.py dnf plugin:
```
$ sudo cp repoquery.py /usr/lib/python3.5/site-packages/dnf-plugins/repoquery.py
```

Run a query with "--graphviz":
```
$ dnf -C -q --disablerepo=* --enablerepo=rawhide repoquery  \
  --arch=noarch,x86_64 --requires --graphviz \
  coreutils systemd bash NetworkManager util-linux kernel-core \
  rpm dnf docker glibc grub2 dracut grep bzip2 gzip xz zlib less \
  iproute chrony openssh-clients procps-ng rsync sed sudo tar \
  subscription-manager filesystem initscripts findutils  \
  > RPMS.dot

```

Make a nice graph svg and display it
```
$ cat RPMS.dot \
  | dot -Gsmoothing=1 -Gstart=3 -Goverlap=prism \
        -Gsplines=spline -Tsvg \
        > RPMS.svg && firefox RPMS.svg

```

Generate statistics on how much diskspace to save, if a component and it's independant dependencies are not needed anymore
```
$ mkdir tt; cd tt
$ python3 ../subtrees.py \
  coreutils systemd bash NetworkManager util-linux kernel-core \
  rpm dnf docker glibc grub2 dracut grep bzip2 gzip xz zlib less \
  iproute chrony openssh-clients procps-ng rsync sed sudo tar \
  subscription-manager filesystem initscripts findutils  \
  > index.html && firefox index.html
```

Now view the results in a nice HTML page.