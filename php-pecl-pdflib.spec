%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}
%{!?php_apiver: %{expand: %%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)}}

%define pecl_name pdflib

Summary:        Package for generating PDF files
Summary(fr):    Extension pour générer des fichiers PDF
Name:           php-pecl-pdflib
Version:        2.1.5
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
%if %{?php_zend_api}0
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}
%else
Requires:     php-api = %{php_apiver}
%endif

%description
This PHP extension wraps the PDFlib programming library
for processing PDF on the fly.

More info on how to use PDFlib with PHP can be found at
http://www.pdflib.com/developer-center/technical-documentation/php-howto


%description -l fr
Cette extension PHP fournit une interface sur la biliothèque de développement
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
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/pdf.ini << 'EOF'
; Enable PDFlib extension module
extension=pdf.so
EOF

# Install XML package description
# use 'name' rather than 'pecl_name' to avoid conflict with pear extensions
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


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
%config(noreplace) %{_sysconfdir}/php.d/pdf.ini
%{php_extdir}/pdf.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sun Sep 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.1.5-2
- rebuild

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
