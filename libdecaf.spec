#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Elliptic curve library
Summary(pl.UTF-8):	Biblioteka krzywych eliptycznych
Name:		libdecaf
Version:	1.0.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://downloads.sourceforge.net/ed448goldilocks/%{name}-%{version}.tgz
# Source0-md5:	48b57dc6ff6be56930f0be2a5722a70e
Patch0:		%{name}-cmake.patch
URL:		http://ed448goldilocks.sourceforge.net/
BuildRequires:	cmake >= 3.0
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel
BuildRequires:	python >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libdecaf library is for elliptic curve research and practical
application. It currently supports Ed448-Goldilocks and Curve25519.

%description -l pl.UTF-8
Biblioteka libdecaf służy do badań i praktycznych zastosowań krzywych
eliptycznych. Obecnie obsługuje Ed448-Goldilocks oraz Curve25519.

%package devel
Summary:	Header files for decaf library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki decaf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for decaf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki decaf.

%package static
Summary:	Static decaf library
Summary(pl.UTF-8):	Statyczna biblioteka decaf
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static decaf library.

%description static -l pl.UTF-8
Statyczna biblioteka decaf.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	%{!?with_static_libs:-DENABLE_STATIC=OFF}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc HISTORY.txt LICENSE.txt README.md TODO.txt
%attr(755,root,root) %{_libdir}/libdecaf.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdecaf.so
%{_includedir}/decaf
%{_includedir}/decaf.h
%{_includedir}/decaf.hxx
%dir %{_datadir}/decaf
%{_datadir}/decaf/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdecaf.a
%endif
