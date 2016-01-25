```
$ sudo cp repoquery.py /usr/lib/python3.5/site-packages/dnf-plugins/repoquery.py

$ dnf -C -q --disablerepo=* --enablerepo=rawhide repoquery  --arch=noarch,x86_64 --requires  --graphviz \
  coreutils systemd bash NetworkManager util-linux kernel-core \
  rpm dnf docker glibc grub2 dracut grep bzip2 gzip xz zlib less \
  iproute chrony openssh-clients procps-ng rsync sed sudo tar \
  subscription-manager filesystem initscripts findutils  \
  | python3 subtrees.py

140312 kB  glibc
125746 kB  glibc-common
 70741 kB  grub2
 70533 kB  subscription-manager
 49923 kB  docker
 46037 kB  grub2-tools
 39240 kB  python3-libs
 34833 kB  systemd
 26254 kB  NetworkManager
 24967 kB  python-libs
 14591 kB  yum
 14453 kB  coreutils
 12922 kB  glib2
 12700 kB  pam
  9923 kB  util-linux
  9885 kB  python3
[…]



$ ls Tree-*.dot
Tree-audit-libs.dot                     Tree-glibc-common.dot               Tree-libpng.dot                Tree-pyliblzma.dot
Tree-bash-completion.dot                Tree-glibc.dot                      Tree-libproxy.dot              Tree-python2-setuptools.dot
Tree-bash.dot                           Tree-glib-networking.dot            Tree-libpwquality.dot          Tree-python3-dnf.dot
Tree-bind99-libs.dot                    Tree-gmp.dot                        Tree-librepo.dot               Tree-python3.dot
Tree-bind99-license.dot                 Tree-gnupg2.dot                     Tree-libreport-filesystem.dot  Tree-python3-hawkey.dot
[…]

$ cat Tree-subscription-manager.dot | dot   -Gsmoothing=1    -Gstart=3 -Goverlap=prism  -Gsplines=spline -Ecolor=#44444455 -Tsvg > foo.svg && firefox foo.svg

```