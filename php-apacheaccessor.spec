%define modname apacheaccessor
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B12_%{modname}.ini

Summary:	Simple API to Apache runtime configuration for PHP
Name:		php-%{modname}
Version:	0.5.1
Release:	%mkrel 2
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/ApacheAccessor/
Source0:	http://pecl.php.net/get/apacheaccessor-%{version}.tgz
Source1:	B12_apacheaccessor.ini
BuildRequires:	pkgconfig
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	apache-devel
BuildRequires:	apr-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ApacheAccessor lets you retrieve Apache configuration (at runtime of current
proccess) as PHP array or dump it as HTML table.

%prep

%setup -q -n apacheaccessor-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild
export CPPFLAGS="`apr-1-config --cppflags`"

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-apxs=/usr/bin/apxs \
    --with-aprconfig=/usr/bin/apr-1-config \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml examples
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 0.5.1-2mdv2012.0
+ Revision: 795397
- rebuild for php-5.4.x

* Mon Apr 02 2012 Oden Eriksson <oeriksson@mandriva.com> 0.5.1-1
+ Revision: 788797
- heh...
- 0.5.1

* Mon Jan 16 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-6
+ Revision: 761685
- a different fix...
- try to fix build
- rebuild
- rebuilt for php-5.3.8
- rebuilt for php-5.3.7
- mass rebuild
- rebuilt for php-5.3.6
- 0.1.1

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-5mdv2011.0
+ Revision: 629761
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-4mdv2011.0
+ Revision: 628060
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-3mdv2011.0
+ Revision: 600457
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2011.0
+ Revision: 588739
- rebuild

* Wed Jul 07 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2011.0
+ Revision: 549839
- import php-apacheaccessor


* Wed Jul 07 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2010.1
- initial Mandriva package
