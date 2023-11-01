Summary: Multipath TCP daemon
Name: mptcpd
Version: 0.8
Release: 3%{?dist}
License: BSD
URL: https://multipath-tcp.org
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: make
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: autoconf-archive
BuildRequires: libell-devel
BuildRequires: systemd-units
BuildRequires: systemd-rpm-macros

Source0: https://github.com/intel/mptcpd/archive/v%{version}/%{name}-%{version}.tar.gz

Patch2: workaround-build-issues-uapi.patch
Patch3: 0003-fix-multilib-install.patch
Patch4: 0001-mptcpize-force-MPTCP-usage-for-IPPROTO_IP-too-159.patch
Patch5: 0001-mptcpize-use-explicit-file-copy-instead-of-rename-16.patch

%description
The Multipath TCP Daemon is a daemon for Linux based operating systems that
performs multipath TCP path management related operations in user space. It
interacts with the Linux kernel through a generic netlink connection to track
per-connection information (e.g. available remote addresses), available network
interfaces, request new MPTCP subflows, handle requests for subflows, etc.

%package devel
Summary: MPTCP path manager header files
Group: Development/Libraries
Requires: pkgconfig
Requires: %{name}%{?_isa} = %{version}-%{release}
License: BSD

%description devel
Header files for adding MPTCP path manager support to applications

%prep
%autosetup -p1

%build
autoreconf --install --symlink --force
%configure --enable-debug=info
%make_build V=1

%install
install -d %{buildroot}/%{_libexecdir}
install -d %{buildroot}/%{_mandir}/man8
install -d %{buildroot}/%{_sysconfdir}/%{name}
install -d %{buildroot}/%{_unitdir}
install -d %{buildroot}/%{_libdir}/%{name}
install -d %{buildroot}/%{_includedir}/%{name}
%make_install
sed -i '/^# addr-flags=subflow/s/^# //g' %{buildroot}/%{_sysconfdir}/%{name}/%{name}.conf
sed -i '/^# notify-flags=existing,skip_link_local,skip_loopback/s/^# //g' %{buildroot}/%{_sysconfdir}/%{name}/%{name}.conf
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%systemd_postun mptcp.service

%files
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%dir %{_sysconfdir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/libmptcpd.so.*
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/libmptcpwrap.so*
%{_libexecdir}/%{name}
%{_bindir}/mptcpize
%{_unitdir}/mptcp.service
%{_mandir}/man8/%{name}.8.gz
%{_mandir}/man8/mptcpize.8.gz
# todo add %doc
%license COPYING

%files devel
%doc COPYING
%dir %{_includedir}/%{name}
%{_libdir}/*.so
%{_includedir}/mptcpd/*.h
%{_libdir}/pkgconfig/mptcpd.pc

%changelog
* Wed Jul  6 2022 Davide Caratti <dcaratti@redhat.com> - 0.8-3
- workaround for uAPI header build issue

* Tue Nov 30 2021 Davide Caratti <dcaratti@redhat.com> - 0.8-2
- fix mptcpize to work also when protocol number is 0 (upstream issue #159)
  and when command resides in another file system (upstream issue #161)
  Related: rhbz#2015623

* Wed Sep 29 2021 Davide Caratti <dcaratti@redhat.com> - 0.8-1
- update to version 0.8

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 0.7-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Jun 23 2021 Davide Caratti <dcaratti@redhat.com> - 0.7-2
- add a simple sanity test and enable gating. Related: rhbz#1962741
- don't overwrite global build options. Related: rhbz#1967697
- fix 'check_conflicts' on multilib. Related: rhbz#1967697

* Wed Apr 28 2021 Davide Caratti <dcaratti@redhat.com> - 0.7-1
- update to version 0.7

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 0.6-2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Mar 17 2021 Davide Caratti <dcaratti@redhat.com> - 0.6-1
- update to version 0.6

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Davide Caratti <dcaratti@redhat.com> - 0.5.1-1
- initial build
