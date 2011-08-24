%define modname apacheaccessor
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B12_%{modname}.ini

Summary:	Simple API to Apache runtime configuration for PHP
Name:		php-%{modname}
Version:	0.1.1
Release:	%mkrel 5
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

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-apxs=/usr/sbin/apxs \
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

