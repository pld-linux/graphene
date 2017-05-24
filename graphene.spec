# NOTE: despite some comments in configure, SSE2 is not selected at runtime;
# SSE2 option seems to change the ABI of library
#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	introspection	# gobject introspection
%bcond_with	sse2		# x86 SSE2 fast paths
%bcond_without	armneon		# ARM NEON fast paths

%ifarch pentium4 %{x8664}
%define	with_sse2	1
%endif
Summary:	Graphene - a thin layer of types for graphic libraries
Summary(pl.UTF-8):	Graphene - cienka warstwa typów dla bibliotek graficznych
Name:		graphene
Version:	1.6.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/graphene/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	4f823f2e6a9849ea2c85d4be52c0326f
Patch0:		%{name}-gcc.patch
URL:		https://github.com/ebassi/graphene
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.40.0
%{?with_introspection:BuildRequires:	gobject-introspection-devel >= 1.41.0}
BuildRequires:	gtk-doc >= 1.20
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.40.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Graphene provides a small set of mathematical types needed to
implement graphic libraries that deal with 2D and 3D transformations
and projections.

%description -l pl.UTF-8
Graphene udostępnia mały zestaw typów matematycznych potrzebnych przy
implementowaniu bibliotek graficznych wykonujących przekształcenia i
rzuty 2D oraz 3D.

%package devel
Summary:	Header files for Graphene library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Graphene
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.40.0

%description devel
Header files for Graphene library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Graphene.

%package static
Summary:	Static Graphene library
Summary(pl.UTF-8):	Statyczna biblioteka Graphene
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Graphene library.

%description static -l pl.UTF-8
Statyczna biblioteka Graphene.

%package apidocs
Summary:	API documentation for Graphene library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Graphene
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Graphene library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Graphene.

%prep
%setup -q
%patch0 -p1

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I build/autotools
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_armneon:--disable-arm-neon} \
	%{!?with_introspection:--disable-introspection} \
	--disable-silent-rules \
	%{!?with_sse2:--disable-sse2} \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgraphene-1.0.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgraphene-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgraphene-1.0.so.0
%if %{with introspection}
%{_libdir}/girepository-1.0/Graphene-1.0.typelib
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgraphene-1.0.so
%{_includedir}/graphene-1.0
%dir %{_libdir}/graphene-1.0
%{_libdir}/graphene-1.0/include
%if %{with introspection}
%{_datadir}/gir-1.0/Graphene-1.0.gir
%endif
%{_pkgconfigdir}/graphene-1.0.pc
%{_pkgconfigdir}/graphene-gobject-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgraphene-1.0.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/graphene
