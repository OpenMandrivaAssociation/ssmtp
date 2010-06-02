%define	name		ssmtp
%define	version		2.64
%define	release		4
%define	src_version	2.64

Summary:	A minimal mail-transfer agent which forwards mail to an SMTP server
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
License:	GPL
URL:		http://packages.debian.org/unstable/mail/ssmtp.html
Group:		System/Servers
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	rcs
BuildRequires:	openssl-devel
Provides:	sendmail-command
Requires:	common-licenses

Source:		http://ftp.debian.org/debian/pool/main/s/ssmtp/%{name}_%{version}.tar.bz2

%description
This is sSMTP, a program that replaces sendmail on workstations that
should send their mail via the departmental mailhub from which they pick up
their mail (via pop, imap, rsmtp, pop_fetch, NFS... or the like).  This
program accepts mail and sends it to the mailhub, optionally replacing the
domain in the From: line with a different one.

%prep
%setup -q

# viet 05/08/2003 / by default, the configure script sets sysconfdir
# to /usr/etc, which is no good. The --sysconfdir= switch doesn't do
# anything either because Makefile.in is not using it => patching Makefile.in
perl -pi -e 's|etcdir=\$\(prefix\)/etc|etcdir=\@sysconfdir\@|' Makefile.in

%build
%serverbuild
%configure --enable-ssl --enable-md5auth
%make

%install
rm -fr %{buildroot}

install -D -m 755 ssmtp		%{buildroot}%{_sbindir}/ssmtp
install -D -m 644 ssmtp.conf	%{buildroot}%{_sysconfdir}/ssmtp/ssmtp.conf
install -D -m 644 revaliases	%{buildroot}%{_sysconfdir}/ssmtp/revaliases
install -D -m 644 ssmtp.conf.5	%{buildroot}%{_mandir}/man5/ssmtp.conf.5
install -D -m 644 ssmtp.8	%{buildroot}%{_mandir}/man8/ssmtp.8

# fix doc permissions:
chmod 644 INSTALL README ChangeLog CHANGELOG_OLD COPYRIGHT TLS *.lsm

#ln -s %{_sbindir}/ssmtp %{buildroot}%{_sbindir}/sendmail
# ln -s %{_mandir}/man8/ssmtp.8.bz2 %{buildroot}%{_mandir}/man8/sendmail.8.bz2
#ln -s ssmtp.8.bz2 %{buildroot}%{_mandir}/man8/sendmail.8.bz2

%clean
rm -fr %{buildroot}

%post
update-alternatives --install %{_sbindir}/sendmail sendmail-command %{_sbindir}/ssmtp 5 --slave %{_prefix}/lib/sendmail sendmail-command-in_libdir %{_sbindir}/ssmtp


%preun
if [ $1 = 0 ]; then
        update-alternatives --remove sendmail-command %{_sbindir}/ssmtp
fi


%files
%defattr(-,root,root)
%doc INSTALL README ChangeLog CHANGELOG_OLD COPYRIGHT TLS *.lsm 
%{_sbindir}/ssmtp
%config(noreplace) %dir %{_sysconfdir}/ssmtp
%config(noreplace) %{_sysconfdir}/ssmtp/*
%{_mandir}/man8/*
%{_mandir}/man5/*
