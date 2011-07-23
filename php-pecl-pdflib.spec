%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}
%{!?php_apiver: %{expand: %%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)}}

%global pecl_name pdflib
%global extname   pdf

Summary:        Package for generating PDF files
Summary(fr):    Extension pour générer des fichiers PDF
Name:           php-pecl-pdflib
Version:        2.1.8
Release:        2%{?dist}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/pdflib

Source:         http://pecl.php.net/get/pdflib-%{version}.tgz

Source2:        xml2changelog

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:       php-pecl(pdflib) = %{version}-%{release}, php-pdflib = %{version}-%{release}
BuildRequires:  php-devel, pdflib-lite-devel, php-pear
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
%if 0%{?php_zend_api:1}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}
%else
Requires:     php-api = %{php_apiver}
%endif

%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
%{?filter_setup:
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}
%endif


%description
This PHP extension wraps the PDFlib programming library
for processing PDF on the fly.

More info on how to use PDFlib with PHP can be found at
http://www.pdflib.com/developer-center/technical-documentation/php-howto


%description -l fr
Cette extension PHP fournit une interface sur la bibliothèque de développement
PDFlib pour générer des fichiers PDF à la volée.

Plus d'informations sur l'utilisation de PDFlib avec PHP sur
http://www.pdflib.com/developer-center/technical-documentation/php-howto


%prep 
%setup -c -q
%{_bindir}/php -n %{SOURCE2} package.xml >CHANGELOG

cd pdflib-%{version}


%build
cd pdflib-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}


%install
cd pdflib-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{extname}.ini << 'EOF'
; Enable PDFlib extension module
extension=%{extname}.so
EOF

# Install XML package description
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}
php -n \
    -d extension_dir=modules \
    -d extension=%{extname}.so \
    --modules | grep %{extname}


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, -)
%doc CHANGELOG pdflib-%{version}/CREDITS
%config(noreplace) %{_sysconfdir}/php.d/%{extname}.ini
%{php_extdir}/%{extname}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sat Jul 23 2013 Remi Collet <rpmfusion@FamilleCollet.com> 2.1.8-1
- fix private-shared-object-provides rpmlint warning
- fix macro usage
- add %%check, minimal load test

* Thu May 06 2010 Remi Collet <rpmfusion@FamilleCollet.com> 2.1.8-1
- update to 2.1.8

* Sat Oct 24 2009 Remi Collet <rpmfusion@FamilleCollet.com> 2.1.7-2
- rebuild

* Tue Jul 14 2009 Remi Collet <rpmfusion@FamilleCollet.com> 2.1.7-1
- update to 2.1.7, rebuild against php 5.3.0

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.6-2
- rebuild for new F11 features

* Thu Mar 19 2009 Remi Collet <RPMS@FamilleCollet.com> 2.1.6-1
- update to 2.1.6

* Sun Sep 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.1.5-2
- rebuild

* Fri Mar 28 2008 Remi Collet <RPMS@FamilleCollet.com> 2.1.5-2
- rebuild against pdflib-lite-7.0.3

* Sat Mar 15 2008 Remi Collet <RPMS@FamilleCollet.com> 2.1.5-1
- update to 2.1.5

* Tue Sep 25 2007 Remi Collet <RPMS@FamilleCollet.com> 2.1.4-2
- add missing BR php-pear

* Tue Sep 25 2007 Remi Collet <RPMS@FamilleCollet.com> 2.1.4-1
- update to 2.1.4
- convert package from v1 to v2
- register extension (new PHP Guidelines)
- remove License file (not provided upstream)

* Sat Mar 17 2007 Remi Collet <RPMS@FamilleCollet.com> 2.1.3-2
- rebuild againt pdflib-lite-7.0.1

* Fri Mar  9 2007 Remi Collet <RPMS@FamilleCollet.com> 2.1.3-1
- requires php(zend-abi) and php(api) when available
- update to 2.1.3

* Sat Dec 09 2006 Remi Collet <RPMS@FamilleCollet.com> 2.1.2-1
- initial spec for Livna
