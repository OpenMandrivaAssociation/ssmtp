%define	name		ssmtp
%define	version		2.61
%define	release		1
%define	src_version	2.61

Summary:	A minimal mail-transfer agent which forwards mail to an SMTP server
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
License:	GPL
URL:		http://packages.debian.org/unstable/mail/ssmtp.html
Group:		System/Servers
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	rcs
Provides:	sendmail-command
Requires:	common-licenses

Source:		http://ftp.debian.org/debian/pool/main/s/ssmtp/%{name}_%{version}.tar.bz2
Patch0:		ssmtp-2.50.3-maxsysuid.patch

%description
This is sSMTP, a program that replaces sendmail on workstations that
should send their mail via the departmental mailhub from which they pick up
their mail (via pop, imap, rsmtp, pop_fetch, NFS... or the like).  This
program accepts mail and sends it to the mailhub, optionally replacing the
domain in the From: line with a different one.

%prep
%setup -q -n %{name}-%{src_version}
# this has to be %patch but it does not work with -g option :(
#%{_bzip2bin} -d < %PATCH0 | patch -p1 -g0 -s
#PATCH_GET=0
#export PATCH_GET
#%patch0 -p1 -b .maxsysuid

# viet 05/08/2003 / by default, the configure script sets sysconfdir
# to /usr/etc, which is no good. The --sysconfdir= switch doesn't do
# anything either because Makefile.in is not using it => patching Makefile.in
perl -pi -e 's|etcdir=\$\(prefix\)/etc|etcdir=\@sysconfdir\@|' Makefile.in

%build
%serverbuild
%configure
%make

%install
rm -fr %{buildroot}

mkdir -p %{buildroot}{%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/ssmtp}

cp ssmtp	%{buildroot}%{_sbindir}/
cp ssmtp.8	%{buildroot}%{_mandir}/man8/
cp ssmtp.conf	%{buildroot}%{_sysconfdir}/ssmtp/
cp revaliases	%{buildroot}%{_sysconfdir}/ssmtp/

#ln -s %{_sbindir}/ssmtp %{buildroot}%{_sbindir}/sendmail
# ln -s %{_mandir}/man8/ssmtp.8.bz2 %{buildroot}%{_mandir}/man8/sendmail.8.bz2
#ln -s ssmtp.8.bz2 %{buildroot}%{_mandir}/man8/sendmail.8.bz2

# Fix perms of %doc files
chmod 644 INSTALL README TLS *.lsm

%clean
rm -fr %{buildroot}

%post
update-alternatives --install %{_sbindir}/sendmail sendmail-command %{_sbindir}/ssmtp 5

%preun
if [ $1 = 0 ]; then
        update-alternatives --remove sendmail-command %{_sbindir}/ssmtp
fi


%files
%defattr(-,root,root)
%doc INSTALL README TLS *.lsm

%doc %attr(0644, root, root) %{_mandir}/man8/ssmtp.8*
#%doc %{_mandir}/man8/sendmail.8*

%attr(0755, root, root) %config(noreplace) %dir %{_sysconfdir}/ssmtp
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/ssmtp/*

%attr(0755, root, root) %{_sbindir}/ssmtp


