# Dash (digital cash) cryptocurrency spec file
# Dash Core QT wallet, masternode, full node, and more.
#
# Note about edits within the spec: Any comments beginning with #t0dd is my
# attempt to block off troublesome, or inappropriate stuff that came over from
# the bitcoin.spec file that this is based off of. Some things, like the SELinux
# elements will likely be brought back in when I get a moment.
#
# Enjoy. Todd Warner <t0dd@protonmail.com>, Winter 2016

%define _hardened_build 1
%global selinux_variants mls strict targeted

# To produce a dashcore-debuginfo package:
#   1. Comment out this define
#   2. Separate the %'s from their variable (this screws things up)
# Otherwise, leave it uncommented
%define debug_package %{nil}

# "bump" refers to "release bump" and is a build identifier For full releases,
# one will often just name this a numberal for every build: 1, 2, 3, etc. For
# more experimental builds, one will often just make it a date 20160405, or a
# date with a numeral, like 20160405.0, 20160405.1, etc.
# Use whatever is meaningful to you. Just remember if you are iterating, it needs
# to be consistent and progress in version (so that upgrades work)
%define bump test.b00772.0

# "bumptag" is used to indicate additional information, usually an identifier,
# like the builder's initials, or a date, or both, or nil.
# Example, the original builder was "taw" or "t0dd Warner", so he could use .taw
# Note: If the value is not %{nil} there needs to be a . preceding this value
# For final releases, one will often opt to nil-out this value.
%define bumptag .taw
#% define bumptag %{nil}

%define _release %{bump}%{bumptag}

%define _name dashcore
Name: dashcore
Version: 0.12.1
Release: %{_release}%{?dist}
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency

# upstream bitcoin team convention - v0.12.1
#%define archivebasename v%{version}
# upstream dash team convention - dashcore-0.12.1
%define archivebasename %{_name}-%{version}
%define sourcetree %{_name}-%{version}

Group: Applications/System
License: MIT
URL: http://dash.org/
# upstream
#Source0: http://github.com/dashpay/%{name}/archive/%{archivebasename}.tar.gz
Source0: %{archivebasename}.tar.gz
# Contributions (not yet in main package)
# dashd.tmpfiles, dash.sysconfig, dash.service, dash.init(never used?)
# Icons, manpages, desktop stuff, etc.
# includes some future SELinux policy stuff as well (.te, .if, .fc)
Source1: %{archivebasename}-contrib.tar.gz
#t0dd Source8:  README.server.redhat
#t0dd Source9:  README.utils.redhat
#t0dd Source10: README.gui.redhat

#t0dd I do not think this is needed for Dash
# Dest change address patch for Lamassu Bitcoin machine
#Patch1: bitcoin-0.12.0-destchange.patch

# patch configure.ac (autoconf template) for fedora builds
#Patch0: %{archivebasename}-fedora.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: gcc-c++
BuildRequires: qt5-qtbase-devel qt5-linguist
BuildRequires: qrencode-devel miniupnpc-devel protobuf-devel openssl-devel
BuildRequires: desktop-file-utils autoconf automake
#BuildRequires: checkpolicy selinux-policy-devel selinux-policy-doc
BuildRequires: boost-devel libdb4-cxx-devel libevent-devel
BuildRequires: libtool java

# ZeroMQ not testable yet on RHEL due to lack of python3-zmq so
# enable only for Fedora
%if 0%{?fedora}
BuildRequires: python3-zmq zeromq-devel
%endif

# Python tests still use OpenSSL for secp256k1, so we still need this to run
# the testsuite on RHEL7, until Red Hat fixes OpenSSL on RHEL7. It has already
# been fixed on Fedora. Bitcoin itself no longer needs OpenSSL for secp256k1.
%if 0%{?rhel}
# via the bitcoin repos, see https://linux.ringingliberty.com/bitcoin/
BuildRequires: openssl-compat-bitcoin-libs
BuildRequires: python34
%endif



# dashcore-client
%package client
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (dash-qt client)


# dashcore-server
%package server
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (dashd server)
Requires(post):	systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
Requires(pre): shadow-utils
Requires(post):	/usr/sbin/semodule, /sbin/restorecon, /sbin/fixfiles
Requires(postun): /usr/sbin/semodule, /sbin/restorecon, /sbin/fixfiles
#t0dd Requires: selinux-policy
#t0dd Requires: policycoreutils-python
Requires: openssl-libs
#Requires: dashcore-utils%{?_isa} = %{version}-%{_release}
#Requires: dashcore-utils = %{version}-%{_release}
#Requires: dashcore-utils = %{version}
Requires: dashcore-utils = %{version}-%{release}


# dashcore-libs
%package libs
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (consensus libraries)


# dashcore-devel
%package devel
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (dev libraries and headers)
#Requires: dashcore-libs%{?_isa} = %{version}-%{_release}
#Requires: dashcore-libs = %{version}-%{_release}
Requires: dashcore-libs = %{version}-%{release}


# dashcore-utils
%package utils
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (commandline utils)



# dashcore SRPM
%description
This is the source package for building the Dash Core set of binary packages.
It will build dashcore-{client,server,utils,libs,devel,debuginfo}.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.



# dashcore-client
%description client
This package provides dash-qt, a user-friendly wallet manager for
personal use.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.


# dashcore-server
%description server
This package provides dashd, a peer-to-peer node and wallet server. It is the
command line installation without a GUI.  It can be used as a commandline wallet
and is typically used to run a Dash Masternode. Requires the dashcore-utils RPM
package to be installed.

If you are running this as a masternode, it is highly recommended that you also
install Sentinel. Read more here: https://github.com/nmarley/sentinel Please refer
to Dash documentation at dash.org for more information about running a Masternode.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.


# dashcore-libs
%description libs
This package provides libbitcoinconsensus, which is used by third party
applications to verify scripts (and other functionality in the future).

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.


# dashcore-devel
%description devel
This package provides the libraries and header files necessary to
compile programs which use libbitcoinconsensus.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.


# dashcore-utils
%description utils
This package provides dash-cli, a utility to communicate with and
control a Dash server via its RPC protocol, and dash-tx, a utility
to create custom Dash transactions.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.



%prep
# dash upstream stuff
%setup -q -n %{sourcetree}
# extra contributions - Source1
%setup -q -T -D -b 1 -n %{sourcetree}
# Patch addressed by removing one dir path level (-p1)
#%patch0 -p1

# Install README files
#t0dd cp -p %{SOURCE8} %{SOURCE9} %{SOURCE10} .

# XXX Prep SELinux policy -- NOT USED YET
# not sure why this is done here in particular -t0dd
mkdir -p SELinux
cp -p ./additions/selinux/dash.{te,if,fc} SELinux

%build
# Build Dash
./autogen.sh
%configure --enable-reduce-exports --enable-glibc-back-compat

make %{?_smp_mflags}

#t0dd # Build SELinux policy
#t0dd pushd SELinux
#t0dd for selinuxvariant in %{selinux_variants}
#t0dd do
#t0dd # FIXME: Create and debug SELinux policy
#t0dd   make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
#t0dd   mv dash.pp dash.pp.${selinuxvariant}
#t0dd   make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
#t0dd done
#t0dd popd


%check
# Run all the tests
#t0dd make check
#t0dd # Run all the other tests
#t0dd pushd src
#t0dd srcdir=. test/dashcore-util-test.py
#t0dd popd
#t0dd LD_LIBRARY_PATH=/opt/openssl-compat-dash/lib PYTHONUNBUFFERED=1  qa/pull-tester/rpc-tests.py -extended


%install
rm -rf %{buildroot}
mkdir %{buildroot}

make INSTALL="install -p" CP="cp -p" DESTDIR=%{buildroot} install

# TODO: Upstream puts dashd in the wrong directory. Need to fix the
# upstream Makefiles to relocate it.
#mkdir -p -m755 %{buildroot}%{_sbindir}
#mv %{buildroot}%{_bindir}/dashd %{buildroot}%{_sbindir}/dashd
install -d -m755 -p %{buildroot}%{_sbindir}
install -D -m755 -p %{buildroot}%{_bindir}/dashd %{buildroot}%{_sbindir}/dashd
rm -f %{buildroot}%{_bindir}/dashd

# Remove the test binaries
# XXX For production release, uncomment the next two lines
#rm -f %{buildroot}%{_bindir}/test_*
#rm -f %{buildroot}%{_bindir}/bench_dash


# Install / config ancillary files
# Remember:
#   %{_datadir} = /usr/share
#   %{_mandir} = /usr/share/man
#   %{_sysconfdir} = /etc
#   %{_localstatedir} = /var
#   %{_sharedstatedir} is /var/lib
#   %{_tmpfilesdir} = /usr/lib/tmpfiles.d
#   %{_unitdir} = /usr/lib/systemd/system
install -d %{buildroot}%{_datadir}
install -d %{buildroot}%{_mandir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_localstatedir}
install -d %{buildroot}%{_sharedstatedir}
install -d %{buildroot}%{_tmpfilesdir}
install -d %{buildroot}%{_unitdir}

cp -a usr/share/* %{buildroot}%{_datadir}/
cp -a etc/* %{buildroot}%{_sysconfdir}/
#install -D -m755 -p %{_unitdir}/* %{buildroot}%{_unitdir}

ls -lh usr/share %{buildroot}%{_datadir}
ls -lh usr/share/applications %{buildroot}%{_datadir}/applications
#install -d -m755 -p %{buildroot}%{_datadir}
# Test the dash GUI desktop semantics
# XXX For production release, comment the next line
desktop-file-validate %{buildroot}%{_datadir}/applications/dash-qt.desktop

install -d -m750 -p %{buildroot}%{_sysconfdir}/dashcore
install -d -m750 -p %{buildroot}%{_sharedstatedir}/dashcore

install -D -m600 -p ./%{_sysconfdir}/sysconfig/dash %{buildroot}%{_sysconfdir}/sysconfig/dash
install -D -m644 -p ./%{_unitdir}/dash.service %{buildroot}%{_unitdir}/dash.service
install -D -m644 -p ./%{_tmpfilesdir}/dash.conf %{buildroot}%{_tmpfilesdir}/


gzip %{buildroot}%{_mandir}/man1/dashd.1
gzip %{buildroot}%{_mandir}/man1/dash-qt.1
gzip %{buildroot}%{_mandir}/man5/dash.conf.5
gzip %{buildroot}%{_mandir}/man5/masternode.conf.5

#t0dd # Install SELinux policy
#t0dd for selinuxvariant in %{selinux_variants}
#t0dd do
#t0dd 	install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
#t0dd 	install -p -m 644 SELinux/dash.pp.${selinuxvariant} \
#t0dd 		%{buildroot}%{_datadir}/selinux/${selinuxvariant}/dash.pp
#t0dd donex


%clean
rm -rf %{buildroot}


# dashcore-server
%pre server
# This is for the case that you run dash core as a service (systemctl start dash)
# %{_sharedstatedir} is /var/lib
getent group dash >/dev/null || groupadd -r dash
getent passwd dash >/dev/null || useradd -r -g dash -d %{_sharedstatedir}/dashcore -s /sbin/nologin -c "Dash Core node, masternode, and wallet server" dash
exit 0


# dashcore-server
%post server
%systemd_post dash.service
#t0dd for selinuxvariant in %{selinux_variants}
#t0dd do
#t0dd 	/usr/sbin/semodule -s ${selinuxvariant} -i \
#t0dd 		%{_datadir}/selinux/${selinuxvariant}/dash.pp \
#t0dd 		&> /dev/null || :
#t0dd done
#t0dd # FIXME This is less than ideal, but until dwalsh gives me a better way...
#t0dd /usr/sbin/semanage port -a -t dash_port_t -p tcp 8332
#t0dd /usr/sbin/semanage port -a -t dash_port_t -p tcp 8333
#t0dd /usr/sbin/semanage port -a -t dash_port_t -p tcp 18332
#t0dd /usr/sbin/semanage port -a -t dash_port_t -p tcp 18333
#t0dd /sbin/fixfiles -R dashcore-server restore &> /dev/null || :
#t0dd /sbin/restorecon -R %{_sharedstatedir}/dashcore || :


# dashcore-server
%posttrans server
/usr/bin/systemd-tmpfiles --create


# dashcore-server
%preun server
%systemd_preun dash.service


# dashcore-server
%postun server
%systemd_postun dash.service
#t0dd if [ $1 -eq 0 ] ; then
#t0dd 	# FIXME This is less than ideal, but until dwalsh gives me a better way...
#t0dd 	/usr/sbin/semanage port -d -p tcp 8332
#t0dd 	/usr/sbin/semanage port -d -p tcp 8333
#t0dd 	/usr/sbin/semanage port -d -p tcp 18332
#t0dd 	/usr/sbin/semanage port -d -p tcp 18333
#t0dd 	for selinuxvariant in %{selinux_variants}
#t0dd 	do
#t0dd 		/usr/sbin/semodule -s ${selinuxvariant} -r dash \
#t0dd 		&> /dev/null || :
#t0dd 	done
#t0dd 	/sbin/fixfiles -R dashcore-server restore &> /dev/null || :
#t0dd 	[ -d %{_sharedstatedir}/dashcore ] && \
#t0dd 		/sbin/restorecon -R %{_sharedstatedir}/dashcore \
#t0dd 		&> /dev/null || :
#t0dd fi



# dashcore-client
%files client
%defattr(-,root,root,-)
%license COPYING
#t0dd %doc README.md README.gui.redhat doc/assets-attribution.md doc/multiwallet-qt.md doc/release-notes.md doc/tor.md dash.conf.example
#t0dd 0.12.0.58 %doc README.md doc/assets-attribution.md doc/multiwallet-qt.md doc/release-notes.md doc/tor.md dash.conf.example
%doc doc/assets-attribution.md doc/multiwallet-qt.md doc/release-notes.md doc/tor.md doc/keepass.md
%{_bindir}/dash-qt
# XXX COMMENT OUT TEST BINARY IF THIS IS A PRODUCTION RELEASE
%{_bindir}/test_dash-qt
%{_datadir}/applications/dash-qt.desktop
%{_datadir}/kde4/services/dash-qt.protocol
%{_datadir}/pixmaps/*
%{_datadir}/icons/*
%{_mandir}/man1/dash-qt.1.gz
%{_mandir}/man5/masternode.conf.5.gz


# dashcore-server
%files server
%defattr(-,root,root,-)
%license COPYING
#t0dd %doc README.md README.server.redhat doc/dnsseed-policy.md doc/release-notes.md doc/tor.md dash.conf.example
#t0dd 0.12.0.58 %doc README.md doc/dnsseed-policy.md doc/release-notes.md doc/tor.md dash.conf.example
%doc doc/dnsseed-policy.md doc/release-notes.md doc/tor.md doc/multiwallet-qt.md doc/guide-startmany.md doc/reduce-traffic.md doc/zmq.md
%dir %attr(750,dash,dash) %{_sharedstatedir}/dashcore
%dir %attr(750,dash,dash) %{_sysconfdir}/dashcore
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/dash
%{_unitdir}/dash.service
%doc SELinux/*
%{_sbindir}/dashd
# XXX COMMENT OUT TEST BINARIES IF THIS IS A PRODUCTION RELEASE
%{_bindir}/test_dash
%{_bindir}/bench_dash
%{_tmpfilesdir}/dash.conf
%{_mandir}/man1/dashd.1.gz
%{_mandir}/man5/dash.conf.5.gz
%{_mandir}/man5/masternode.conf.5.gz
#t0dd %{_datadir}/selinux/*/dash.pp


# dashcore-libs
%files libs
%defattr(-,root,root,-)
%license COPYING
#t0dd 0.12.0.58 %doc README.md
%{_libdir}/libbitcoinconsensus.so*


# dashcore-devel
%files devel
%defattr(-,root,root,-)
%license COPYING
#t0dd 0.12.0.58 %doc README.md
%{_includedir}/bitcoinconsensus.h
%{_libdir}/libbitcoinconsensus.a
%{_libdir}/libbitcoinconsensus.la
%{_libdir}/pkgconfig/libbitcoinconsensus.pc


# dashcore-utils
%files utils
%defattr(-,root,root,-)
%license COPYING
#t0dd %doc README.md README.utils.redhat dash.conf.example
#t0dd 0.12.0.58 %doc README.md dash.conf.example
%{_bindir}/dash-cli
%{_bindir}/dash-tx


# More information about DashCore Testnet:
# Announcement message: https://www.dash.org/forum/threads/12-1-testnet-testing-phase-two-ignition.10818/
# Testnet documentation: https://dashpay.atlassian.net/wiki/display/DOC/Testnet
# Testnet masternode documentation: https://gist.github.com/taw00/e978f862ee1ad66722e16bcc8cf18ca5
#
# Latest source builds: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-latestSuccessful/
# Direct source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00<BUILD ID>
# GitHub: https://github.com/dashpay/dash
# GitHub for Sentinel (complimentary to dashd): https://github.com/nmarley/sentinel

%changelog
* Thu Jan 12 2017 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00772.0
- Testnet - Testing Phase 2 -- From build 00772, v0.12.1.0-gf995a26
- f61f6fe59cc8959c947ad9b49850f3989a895813055f143c012f8a4a053616b3  dashcore-0.12.1.tar.gz
-
* Thu Jan 12 2017 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00771.0
- Testnet - Testing Phase 2 -- From build 00771, v0.12.1.0-ge847967
- db37c869a5c2aa5c2dd8d144ab0ff653ad4a69ed018b57730177f2cd942f3f90  dashcore-0.12.1.tar.gz
-
* Thu Jan 12 2017 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00770.1
- Testnet - Testing Phase 2 -- From build 00770, v0.12.1.0-g5cb6486
- 5025679352d9d38c799436cb01f92984bd3d00653ad0aa4bd233d15a037a8f6e  dashcore-0.12.1.tar.gz
- f225678d467cdff3ec9d1e6616ed966e6dcc940d95328208b94ce9b9c11df521  dashcore-0.12.1-contrib.tar.gz
- Removed a bunch of test echos in the spec file (oops!).
- Moved server daemon configuration configuration datadir default to /var/lib/dashcore/ for 12.1
-
* Tue Jan 10 2017 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00770.0
- Testnet - Testing Phase 2 -- From build 00770, v0.12.1.0-g5cb6486
- SHA256: 5025679352d9d38c799436cb01f92984bd3d00653ad0aa4bd233d15a037a8f6e  dashcore-0.12.1.tar.gz
-
* Tue Jan 10 2017 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00768.0
- Testnet - Testing Phase 2 -- From build 00768, v0.12.1.0-g3b9a748
- SHA256: 8701b1044339aaa76fe060c05a0e9e2f3950215719cc36969846845d152a348d  dashcore-0.12.1.tar.gz
-
* Thu Jan 05 2017 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00766.2
- Testnet - Testing Phase 2 -- From build 00766, v0.12.1.0-g7e9ad0e
- SHA256: a5d4c9598bfa0d1eaabfa820f9419dac319c7e12acb9e976d4e178a171fb1d23  dashcore-0.12.1.tar.gz
- Merged contributing tarballs.
- Created and added a pile of desktop icons to better meet industry standards.
-
* Thu Jan 05 2017 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00766.0
- Testnet - Testing Phase 2 -- From build 00766, v0.12.1.0-g7e9ad0e
- SHA256: a5d4c9598bfa0d1eaabfa820f9419dac319c7e12acb9e976d4e178a171fb1d23  dashcore-0.12.1.tar.gz
- No changes to the additional source tarballs.
-
* Tue Jan 03 2017 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00765.0
- Testnet - Testing Phase 2 -- From build 00765, v0.12.1.0-gba8d8ae
- SHA256: 76fe77638472fa7174e45a0505907f31c06f8894d172db042c3c0e17823c9a61  dashcore-0.12.1.tar.gz
- No changes to the additional source tarballs.
-
* Tue Jan 03 2017 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00763.1
- Testnet - Testing Phase 2 -- From build 00763, v0.12.1.0-g457c200
- SHA256: adf9d6b8695d0fedba1d1eac1e66e00ff7cfdf616a00d0f53dcb3e7cb4c42a1f  dashcore-0.12.1.tar.gz
- No changes to the additional source tarballs.
-
- Fix sytem groupadd and sysem useradd -- I commented them out when I should not have. It broke
- loading dash as a service.
-
* Sun Jan 01 2017 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00763.0
- Testnet - Testing Phase 2 -- From build 00763, v0.12.1.0-g457c200
- SHA256: adf9d6b8695d0fedba1d1eac1e66e00ff7cfdf616a00d0f53dcb3e7cb4c42a1f  dashcore-0.12.1.tar.gz
- No changes to the additional source tarballs.
-
* Sat Dec 31 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00757.0
- Testnet - Testing Phase 2 -- From build 00757, v0.12.1.0-g7544a70
- SHA256: fa347dff2ad0ac57a63d73057d7d7cdf6589d76c41bb64505562d800aa9eef98  dashcore-0.12.1.tar.gz
- No changes to the additional source tarballs.
-
* Fri Dec 30 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00756.0
- Testnet - Testing Phase 2 -- From build 00756, v0.12.1.0-g96dda27
- SHA256:
- 60afb2f4d67f6a2071b0646ac485045450d4753dc1fa8212944aeec0d1a17320  dashcore-0.12.1.tar.gz
- 362d950219ce60ca2b45acda1b94b50d305789c2c001a7203dd13946b5da8c60  dashcore-0.12.1-contrib-extras.tar.gz
- c63cf7313cdb01eb0a14f0b4108aab94d1ea740b9cc6160a12cb1a9f4f11c9ba  dashcore-0.12.1-contrib-fedora.tar.gz
- f945bd0f394b292223460cb063c432797f9f52dfad73141a11332a935dcfb5be  dashcore-0.12.1-dashify-extra-qt-icons.tar.gz
- f4714741df69fa3ca785f509eecd2dd678d2c3f364aeb8102edf503350e44e57  dashcore-0.12.1-dashify-pixmaps.tar.gz
-
* Wed Dec 28 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00755.0
- Testnet - Testing Phase 2 -- From build 00755, v0.12.1.0-geddfa5a
- SHA256: c0fdff31584c4b85233a8f82d92027d5f895bbc0844ea3125e2407b0e7e02ed5 dashcore-0.12.1.tar.gz
-
* Mon Dec 26 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00754.0
- Testnet - Testing Phase 2 -- From build 00754, v0.12.1.0-g32d5f4b
- SHA256: 6f76c1058db3966916dd61afa175c13c2e6c5e91880d45c30efa6f2775095643 dashcore-0.12.1.tar.gz
-
* Sat Dec 24 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00752.0
- Testnet - Testing Phase 2 -- From build 00752, v0.12.1.0-g70b3740
- SHA256: 6d3ea1ef8f9fe916f7fa0bef9bf8115da62d7467518407f68467ed2614b6e000 dashcore-0.12.1.tar.gz
-
* Wed Dec 21 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00751.0
- Testnet - Testing Phase 2 -- From build 00751, v0.12.1.0-gc438e74
- SHA256: 7ec66b27f567c4a933d88befd5330148cf9290e11568b71cbdd1e15fbf18a2d8 dashcore-0.12.1.tar.gz
-
* Wed Dec 21 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00750.0
- Testnet - Testing Phase 2 -- From build 00750, v0.12.1.0-g1c6c0d8
- SHA256: 6970d8d0f035c6c296a799a66e88ad1fafdb4046230ef02f15b0af61fcdf493a dashcore-0.12.1.tar.gz
-
* Fri Dec 16 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00744.0
- Testnet - Testing Phase 2 -- From build 00744, v0.12.1.0-g88ee7a3
- SHA256: 4290c4e0aa8413bc736ac0b1d488f18d0e111b9845e99231144afbdc6409a061 dashcore-0.12.1.tar.gz
-
* Wed Dec 14 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00741.3
- Testnet - Testing Phase 2 -- From build 00741, v0.12.1.0-g30da3f5
- SHA256: 71cf52945daabcb801866af72d95c16c37e1fd3055daf1d0989628a962c40ea4 dashcore-0.12.1.tar.gz
- 741.1, 741.2, 741.3: Fix broken Requires. Tighten-up requires between packages.
-
* Mon Dec 12 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00741.0
- Testnet - Testing Phase 2 -- From build 00741, v0.12.1.0-g30da3f5
- SHA256: 71cf52945daabcb801866af72d95c16c37e1fd3055daf1d0989628a962c40ea4 dashcore-0.12.1.tar.gz
-
* Sat Dec 10 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00737.1
- Testnet - Testing Phase 2 -- From build 00737, v0.12.1.0-ga11bd2c
- SHA256: afb137d1a14dab216723b26813e70d243f878031a3407d5747538b711729f987 dashcore-0.12.1.tar.gz
- Added a masternode.conf manpage. Edited the other manpages. Beefed up the
- dash.conf example a bit. And renamed the debian contrib tarball to extras.
-
* Fri Dec 9 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00737.0
- Testnet - Testing Phase 2 -- From build 00737, v0.12.1.0-ga11bd2c
- SHA256: afb137d1a14dab216723b26813e70d243f878031a3407d5747538b711729f987 dashcore-0.12.1.tar.gz
-
* Wed Dec 7 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00735.0
- Testnet - Testing Phase 2 -- From build 00735, v0.12.1.0-g4dac002
- SHA256: 10588a082a97f7e6d8d390bbae0e72437eda76b1ec466d9075e52f9bbf049a28 dashcore-0.12.1.tar.gz
-
* Mon Dec 5 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00731.0
- Testnet - Testing Phase 2 -- From build 00731, v0.12.1.0-g0e28de7
- SHA256: 9dbe2a930acecdbc2ec15ad55c7f3416405f7f7bb59f076b9066664c0bbaeda3 dashcore-0.12.1.tar.gz
-
* Sun Dec 4 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00729.0
- Testnet - Testing Phase 2 -- From build 00729, v0.12.1.0-g786f17e
- SHA256: 3e95a5b465c2e55b419efb0a9fd2c4bf8ae5780350d03e2c4ac4004d304323ad dashcore-0.12.1.tar.gz
-
* Wed Nov 30 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00721.0
- Testnet - Testing Phase 2 -- From build 00721, v0.12.1.0-g6d9e414
- SHA256: 7ce04e4b02ee54a149280127db318d7f14dbacbe3bd9c04bb3ac373cf1e10ac7 dashcore-0.12.1.tar.gz
-
* Sun Nov 27 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00715.0
- Testnet - Testing Phase 2 -- From build 00715, v0.12.1.0-gecdc160
- SHA256: 8ddaf135e0072520e81e27f6e6170f33bacf935c0ce9d2f2204383c46240b1e7 dashcore-0.12.1.tar.gz
-
* Fri Nov 25 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00714.0
- Testnet - Testing Phase 2 -- From build 00714, v0.12.1.0-g1b90d66
- SHA256: c173a9f0c1a9a1d21d733aad8ccd3b5ffe90b600c243c36a0daa416dd23c9f60 dashcore-0.12.1.tar.gz
-
* Wed Nov 23 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00712.0
- Testnet - Testing Phase 2 -- From build 00712, v0.12.1.0-gec59862
- SHA256: 35314fea1f4d002e5e011bfbb3bd14d9e10421b3451a51c07647b6de9f274cfc dashcore-0.12.1.tar.gz
-
* Fri Nov 18 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00706.0
- Testnet - Testing Phase 2 -- From build 00706, v0.12.1.0-ge59bee8
- SHA256: b2f90a4b667737da5d2661ca5952c9ecec51c2ec9d7bf44707c9532a73c5cbbd dashcore-0.12.1.tar.gz
-
* Thu Nov 17 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00705.0
- Testnet - Testing Phase 2 -- From build 00705, v0.12.1.0-g73568be
- SHA256: 8a63d216b901ad966f192410448c6e9803ce5f2c84863e83f03988885e8bb666 dashcore-0.12.1.tar.gz
- RHEL7/CentOS7 needs BuildRequires: openssl-compat-bitcoin-libs in order to run test suites.
- ZeroMQ BuildRequires was missing. Fixed.
- Successful builds for Fedora 24, 25, and CentOS7.
-
* Wed Nov 16 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00702.0
- Testnet - Testing Phase 2 -- From build 00702, v0.12.1.0-g5128085
- SHA256: 7e155ea091fd94abe28ce45372b5f8418d92c21c9eeb48a3ae4adb3bd5340683 dashcore-0.12.1.tar.gz
-
* Tue Nov 15 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00700.0
- Testnet - Testing Phase 2 -- From build 00700, v0.12.1.0-g714f9a4
- SHA256: a338d9692ea0e73a5201586df4f01986ce29fd689383c1196475a62f4ae25696 dashcore-0.12.1.tar.gz
-
* Sun Nov 13 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00699.0
- Testnet - Testing Phase 2 -- From build 00699, v0.12.1.0-gc31ba8b
- SHA256: 58ef36c35e7d6d7fb8c0bb626ec8e7fadc7b8938f9673bef74311c542b5e154d dashcore-0.12.1.tar.gz
-
* Sat Nov 12 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00698.0
- Testnet - Testing Phase 2 -- From build 00698, v0.12.1.0-g82ca5fd
- SHA256: 566b4aac1d361da7797a115c7a2c7f4769f1fbf73cc1f14f581a870e6cc4423a dashcore-0.12.1.tar.gz
-
* Fri Nov 11 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00697.0
- Testnet - Testing Phase 2 -- From build 00697, v0.12.1.0-gd2f1fd2
- SHA256: 556f4e5e6c8b4c11a67d2dc6d0c3bb57112f1cde75b3b9d77c179869d8fd979d dashcore-0.12.1.tar.gz
-
* Tue Nov 08 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00696.0
- Testnet - Testing Phase 2 -- From build 00696, v0.12.1.0-gf21c7cc
- SHA256: 98442787d35037ac7d211253c10f8d3b7b9935103bce162c450aab98f4f56a10 dashcore-0.12.1.tar.gz
-
* Mon Nov 07 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00695.0
- Testnet - Testing Phase 2 -- From build 00695, v0.12.1.0-gb11cc8f
- SHA256: 9032cbbe55a8832a32d8313657b31ce816302736a4aca0df6c93ed728d15af5f dashcore-0.12.1.tar.gz
-
* Sun Nov 06 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00694.0
- Testnet - Testing Phase 2 -- From build 00694
- SHA256: 26502c21a0c01f4838fa0062c7be1ad95d6d238d10d2b9fa6ebba5a2e8c7dad1 dashcore-0.12.1.tar.gz
-
* Wed Nov 02 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00691.0
- Testnet - Testing Phase 2 -- From build 00691
- SHA256: 933d6b9f1fdbff336ff19955ba7ceabc915dc760a0d7cd8dce43fbb3fd75bfd1  dashcore-0.12.1.tar.gz
-
* Mon Oct 31 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00688.0
- Testnet - Testing Phase 2 -- From build 00688
- Upstream packaging change dash-0.12.1.tar.gz becomes... dashcore-0.12.1.tar.gz
- SHA256: 7044b80c0a7254c1780c057cd69fbc5d2bfc53293f4eb86b1c87a9abb8af8d42  dashcore-0.12.1.tar.gz
- Loads of merges.
-
* Thu Oct 27 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00679.0
- Testnet - Testing Phase 2 -- From build 00679
-
* Wed Oct 26 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00676.0
- Testnet - Testing Phase 2 -- From build 00676
-
* Mon Oct 24 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00672.0
- Testnet - Testing Phase 2 -- From build 00672
-
* Sun Oct 23 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00671.0
- Testnet - Testing Phase 2 -- From build 00671
- PrivateSend mixing works once again in this release.
-
* Sun Oct 23 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00670.0
- Testnet - Testing Phase 2 -- From build 00670
-
* Fri Oct 21 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00668.0
- Testnet - Testing Phase 2 -- From build 00668
-
* Fri Oct 21 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00667.0
- Testnet - Testing Phase 2 -- From build 00667
-
* Tue Oct 18 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00666.0
- Testnet - Testing Phase 2 -- From build 00666
-
* Thu Oct 13 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00662.0
- Testnet - Testing Phase 2 -- From build 00662
-
* Sat Oct 08 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00655.0
- Testnet - Testing Phase 2 -- From build 00655
- Apologies for the changing versioning scheme. I can't seem to settle on something I like.
-
* Sun Oct 02 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-1test
- Testnet - Testing Phase 2 -- From the September 30, 2016 build
-
* Thu Sep 29 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-0test
- Testnet - Testing Phase 2 -- From the September 27, 2016 build
- Updated build requirements. Updated descriptions. Updated versioning (yet again).
- Added test binaries.
-
* Mon Sep 26 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-b9bd116.taw_TESTNET20160926
- Testnet Testing Phase 2 - don't use this version
-
* Tue Sep 20 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-TESTNET20160920.taw
- Initial spec - don't use this version
- Note: all kinds of unnatural things done with contrib/* and contrib/fedora copied over from 0.12.0.58
-
