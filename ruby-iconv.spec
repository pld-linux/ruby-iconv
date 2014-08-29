%define pkgname iconv
Summary:	iconv wrapper library
Name:		ruby-%{pkgname}
Version:	1.0.4
Release:	1
License:	MIT/Ruby License
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	f0009c4b1031ba86688aa7964dae319c
URL:		https://github.com/nurse/iconv
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
Conflicts:	ruby-modules < 1:2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
iconv wrapper library.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

cd ext/%{pkgname}
%{__ruby} extconf.rb
%{__make} \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} -fPIC"

# UTF8 locale needed for doc generation
export LC_ALL=en_US.UTF-8
rdoc --ri --op ri lib
rdoc --op rdoc lib
rm -r ri/{Hash,Logging,Object,ri}
rm ri/created.rid
rm ri/cache.ri
rm ri/{page-Makefile.ri,page-mkmf_log.ri}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_vendorarchdir}/iconv,%{ruby_specdir},%{ruby_ridir},%{ruby_rdocdir}}

install -p ext/%{pkgname}/%{pkgname}.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}/iconv
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a ext/%{pkgname}/ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a ext/%{pkgname}/rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%{ruby_vendorlibdir}/iconv.rb
%{ruby_vendorlibdir}/iconv
%dir %{ruby_vendorarchdir}/iconv
%attr(755,root,root) %{ruby_vendorarchdir}/iconv/iconv.so
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Iconv
