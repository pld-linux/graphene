# NOTE: despite some comments in configure, SSE2 is not selected at runtime;
# SSE2 option seems to change the ABI of library
#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	introspection	# gobject introspection
%bcond_with	sse2		# x86 SSE2 fast paths
%bcond_without	armneon		# ARM NEON fast paths
#
%ifarch pentium4 %{x8664}
%define	with_sse2
%endif
Summary:	Graphene - a thin layer of types for graphic libraries
Summary(pl.UTF-8):	Graphene - cienka warstwa typów dla bibliotek graficznych
Name:		graphene
Version:	0.99.2
Release:	2
License:	MIT
Group:		Libraries
Source0:	https://github.com/ebassi/graphene/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ccd4e4d991fb41ff163b1e27cfc41ea2
Patch0:		%{name}-bench.patch
Patch1:		%{name}-gcc.patch
URL:		https://github.com/ebassi/graphene
BuildRequires:	glib2-devel >= 1:2.40.0
%{?with_introspection:BuildRequires:	gobject-introspection-devel >= 1.41.0}
BuildRequires:	gtk-doc >= 1.20
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	pkgconfig
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I build/autotools
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_armneon:--disable-arm-neon} \
	--disable-silent-rules \
	%{!?with_sse2:--disable-sse2} \
	%{?with_static_libs:--enable-static}
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
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libgraphene-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgraphene-1.0.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgraphene-1.0.so
%{_includedir}/graphene-1.0
%{_pkgconfigdir}/graphene-1.0.pc
%{_pkgconfigdir}/graphene-gobject-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgraphene-1.0.a
%endif
