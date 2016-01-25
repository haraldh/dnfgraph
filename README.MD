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
$ python3 subtrees.py < RPMS.dot

140312 kB  glibc (2 packages)
125746 kB  glibc-common (1 packages)
 70741 kB  grub2 (14 packages)
 70533 kB  subscription-manager (58 packages)
 49923 kB  docker (11 packages)
 46037 kB  grub2-tools (5 packages)
 39240 kB  python3-libs (1 packages)
 34833 kB  systemd (7 packages)
 26254 kB  NetworkManager (26 packages)
 24967 kB  python-libs (1 packages)
 14591 kB  yum (28 packages)
 14453 kB  coreutils (3 packages)
 12922 kB  glib2 (2 packages)
 12700 kB  pam (4 packages)
  9923 kB  util-linux (4 packages)
[…]
```


Display the tree of the removed subcomponents
```
$ ls Tree-*.dot
Tree-audit-libs.dot                     Tree-glibc-common.dot               Tree-libpng.dot                Tree-pyliblzma.dot
Tree-bash-completion.dot                Tree-glibc.dot                      Tree-libproxy.dot              Tree-python2-setuptools.dot
Tree-bash.dot                           Tree-glib-networking.dot            Tree-libpwquality.dot          Tree-python3-dnf.dot
Tree-bind99-libs.dot                    Tree-gmp.dot                        Tree-librepo.dot               Tree-python3.dot
Tree-bind99-license.dot                 Tree-gnupg2.dot                     Tree-libreport-filesystem.dot  Tree-python3-hawkey.dot
[…]

$ cat Tree-subscription-manager.dot \
  | dot -Gsmoothing=1 -Gstart=3 -Goverlap=prism \
        -Gsplines=spline -Tsvg \
        > foo.svg && firefox foo.svg

```