Name:           gnote
Version:        0.6.3
Release:        3%{?dist}
Summary:        Note-taking application
Group:          User Interface/Desktops
License:        GPLv3+
URL:            http://live.gnome.org/Gnote
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gnote/0.6/%{name}-%{version}.tar.bz2

# https://bugzilla.redhat.com/show_bug.cgi?id=589189
# Translation updates; most already upstream
Patch1:         gnote-0.6.3-translation.patch
# Additional translations for "Take notes" extracted from upstream .po files
# (panel tooltip was changed immediately before 0.6.3 release)
Patch2:         gnote-0.6.3-take-notes.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  gtkmm24-devel libxml2-devel GConf2-devel intltool 
BuildRequires:  boost-devel libuuid-devel dbus-c++-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gnome-doc-utils >= 0.3.2
BuildRequires:  libpanelappletmm-devel
BuildRequires:  gettext pcre-devel
BuildRequires:  gtkspell-devel

Requires(pre)  :GConf2
Requires(post) :GConf2
Requires(preun):GConf2

%description
Gnote is a desktop note-taking application which is simple and easy to use.
It lets you organize your notes intelligently by allowing you to easily link
ideas together with Wiki style interconnects. It is a port of Tomboy to C++ 
and consumes fewer resources.

%prep
%setup -q

%patch1 -p1 -b .translation
%patch2 -p1 -b .take-notes

%build
%configure --disable-schemas-install --disable-static --with-gnu-ld --enable-dbus
V=1 make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

desktop-file-install \
 --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}/%{_datadir}/applications/gnote.desktop

%find_lang %{name}

%clean
rm -rf %{buildroot}

%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gnote.schemas > /dev/null || :
fi

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
    %{_sysconfdir}/gconf/schemas/gnote.schemas > /dev/null
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gnote.schemas >/dev/null;
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING README TODO NEWS AUTHORS
%{_bindir}/gnote
%{_prefix}/libexec/gnote-applet 
%{_mandir}/man1/gnote.1.gz
%{_datadir}/applications/gnote.desktop
%{_datadir}/gnote/
%{_datadir}/icons/hicolor/*/apps/gnote.png
%{_datadir}/icons/hicolor/scalable/apps/gnote.svg
%{_sysconfdir}/gconf/schemas/gnote.schemas
%{_datadir}/gnome/help/gnote/
%{_datadir}/omf/gnote/
%{_prefix}/%{_lib}/gnote/
%{_prefix}/%{_lib}/bonobo/servers/GNOME_GnoteApplet.server
%{_datadir}/dbus-1/services/org.gnome.Gnote.service

%changelog
* Wed Jun 23 2010 Owen Taylor <otaylor@redhat.com> - 0.6.3-3
- Add translation updates
  Resolves: rhbz 575696

* Fri Jan  8 2010 Owen Taylor <otaylor@redhat.com> - 0.6.3-2
- Fix some rpmlint warnings for spec file 
  Resolves: rhbz 553682

* Tue Dec 02 2009 Rahul Sundaram  <sundaram@fedoraproject.org> 0.6.3-1
- Update to 0.6.3

* Thu Aug 13 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.2-1
- Very minor bug fixes
- http://mail.gnome.org/archives/gnote-list/2009-August/msg00006.html

* Sat Aug 01 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.1-1
- D-Bus support enabled, many new features and bug fixes
- http://mail.gnome.org/archives/gnote-list/2009-July/msg00016.html
- 0.6.0 skipped due to applet breakage fixed in this release
- http://mail.gnome.org/archives/gnote-list/2009-July/msg00020.html

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.5.3-1
- Few minor bug fixes
- http://mail.gnome.org/archives/gnote-list/2009-July/msg00002.html

* Sat Jul 04 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.5.2-2
- Build requires libuuid-devel instead of e2fsprogs-devel

* Sat Jul 04 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.5.2-1
- New upstream bug fix release
- http://mail.gnome.org/archives/gnote-list/2009-July/msg00000.html

* Thu Jun 25 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.5.1-1
- Fixes a regression and some bugs
- http://mail.gnome.org/archives/gnote-list/2009-June/msg00002.html

* Wed Jun 17 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.5.0-1
- Adds the ability to import Tomboy notes on first run 
- http://mail.gnome.org/archives/gnote-list/2009-June/msg00000.html
 
* Thu May 28 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.4.0-1
- Many minor bug fixes from new upstream release
  http://www.figuiere.net/hub/blog/?2009/05/27/670-gnote-040

* Wed May 06 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.3.1-1
- new upstream release. Fixes rhbz #498739. Fix #499227

* Fri May 01 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.3.0-1
- new upstream release. Includes applet and more plugins.

* Fri Apr 24 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.0-2
- enable spell checker

* Thu Apr 23 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.0-1
- new upstream release

* Thu Apr 16 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.2-2
- Add BR on gnome-doc-utils

* Wed Apr 15 2009 Jesse Keating <jkeating@redhat.com> - 0.1.2-1
- Update to 0.1.2 to fix many upstream bugs
  http://www.figuiere.net/hub/blog/?2009/04/15/660-gnote-012

* Fri Apr 10 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.1-4
- Drop a unnecessary require, BR and fix summary

* Wed Apr 08 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.1-3
- Fix review issues

* Wed Apr 08 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.1-2
- include pre script for gconf schema

* Wed Apr 08 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.1-1
- Initial spec file

