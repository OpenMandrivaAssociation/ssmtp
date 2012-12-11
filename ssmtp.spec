%define	src_version	2.64

Summary:	A minimal mail-transfer agent which forwards mail to an SMTP server
Name:		ssmtp
Version:	2.64
Release:	6
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
export LIBS="-lcrypto"
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


%changelog
* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 2.64-5mdv2011.0
+ Revision: 614974
- the mass rebuild of 2010.1 packages

* Wed Jun 02 2010 Ahmad Samir <ahmadsamir@mandriva.org> 2.64-4mdv2010.1
+ Revision: 546920
- revert wrong change of config files, now they're noreplace again
- fix doc permissions, fixes (mdv#59583)

* Sat Apr 24 2010 Bogdano Arendartchuk <bogdano@mandriva.com> 2.64-3mdv2010.1
+ Revision: 538401
- enabled ssl and md5auth

* Fri Feb 12 2010 Ahmad Samir <ahmadsamir@mandriva.org> 2.64-2mdv2010.1
+ Revision: 504815
- clean spec
- add the ssmtp.conf man page

* Tue Jan 19 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.64-1mdv2010.1
+ Revision: 493707
- ssmtp 2.64
- drop obsolete patches
- fix installation of sendmail alternative

* Tue Sep 08 2009 Thierry Vignaud <tv@mandriva.org> 2.62-3mdv2010.0
+ Revision: 434107
- rebuild

* Tue Sep 09 2008 Frederik Himpe <fhimpe@mandriva.org> 2.62-2mdv2009.0
+ Revision: 283189
- Add Gentoo patch fixing security issue CVE-2008-3962

* Sat Jun 14 2008 Jérôme Soyer <saispo@mandriva.org> 2.62-1mdv2009.0
+ Revision: 219152
- New release 2.62

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 2.61-1mdv2008.1
+ Revision: 140851
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix man pages extension


* Sun Feb 18 2007 Jérôme Soyer <saispo@mandriva.org> 2.61-1mdv2007.0
+ Revision: 122490
- New release 2.61
- Import ssmtp

* Fri Mar 17 2006 Michael Scherer <misc@mandriva.org> 2.60.7-3mdk
- use the correct name for alternative, thanks couriousous for spotting this

* Sat Jul 02 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 2.60.7-2mdk
- provides and alternative sendmail-command
- use mkrel
- fix summary-ended-with-dot

* Tue Apr 20 2004 Michael Scherer <misc@mandrake.org> 2.60.7-1mdk 
- 2.60.7, security fix

