%define beta beta1

Name:		freeciv
Version:	2.4.0
%if "%beta" != ""
Release:	0.%beta.1
Source0:	http://download.gna.org/freeciv/beta/freeciv-%version-%beta.tar.bz2
%else
Release:	1
Source0:	http://download.gna.org/freeciv/stable/freeciv-%version.tar.gz
%endif
Summary:	CIVilization clone
License:	GPLv2+
Group:		Games/Strategy
URL:		http://www.freeciv.org/
Source1:	%{name}.server.wrapper
Source2:	stdsounds3.tar.gz
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	readline-devel
BuildRequires:	desktop-file-utils
BuildRequires:	ggz-gtk-client-devel
BuildRequires:	libstdc++-static-devel
Requires(post):	ggz-client-libs
Requires(preun): ggz-client-libs

%description
Freeciv is a multiplayer strategy game, released under the GNU General
Public License. It is generally comparable with Civilization II(r),
published by Microprose(r).

Default configuration uses the Civilization II(r) style Isometric view. If
you prefer classic Civilization(r) 2-d view, invoke the client with
"civclient --tiles trident".

%package	data
Group:		Games/Strategy
Summary:	FREE CIVilization clone - data files
Requires:	%{name}-server = %{version}
BuildArch:	noarch

%description	data
Freeciv is a multiplayer strategy game, released under the GNU General
Public License. It is generally comparable with Civilization II(r),
published by Microprose(r).

Default configuration uses the Civilization II(r) style Isometric view. If
you prefer classic Civilization(r) 2-d view, invoke the client with
"civclient --tiles trident".

%package	client
Group:		Games/Strategy
Summary:	FREE CIVilization clone - client
Provides:	%{name} = %{version}-%{release}
Requires:	%{name}-data = %{version}
Requires:	%{name}-server = %{version}
Obsoletes:	%{name}-client < %{version}-%{release}
Requires(post):	ggz-client-libs
Requires(preun): ggz-client-libs

%description	client
This is the graphical client for freeciv

%package	server
Group:		Games/Strategy
Summary:	FREE CIVilization clone - server
Provides:	%{name} = %{version}-%{release}
Requires:	%{name}-data = %{version}
Requires(post):	ggz-client-libs
Requires(preun): ggz-client-libs

%description	server
This is the server for freeciv.

%prep
%if "%beta" != ""
%setup -q -n %name-%version-%beta
%else
%setup -q
%endif

%build
#locales are not in %{_gamesdatadir}
export localedir=%{_datadir}/locale

%configure2_5x \
    --bindir=%{_gamesbindir} \
    --datadir=%{_gamesdatadir} \
    --enable-client=gtk-2.0
%make

%install
%__rm -rf %{buildroot}
%makeinstall_std localedir=%{_datadir}/locale

tar -xvf %{SOURCE2} -C %{buildroot}%{_gamesdatadir}/%{name}

# wrapper
%__mv %{buildroot}%{_gamesbindir}/freeciv-server %{buildroot}%{_gamesbindir}/civserver.real
%__install -m 755 %{SOURCE1} %{buildroot}%{_gamesbindir}/freeciv-server

# fix icons locations
%__mv %{buildroot}%{_gamesdatadir}/icons %{buildroot}%{_datadir}/icons

# menu entry
desktop-file-install --vendor="" \
			--remove-category="Application" \
			--remove-category="GNOME" \
			--remove-category="Strategy" \
			--add-category="GTK" \
			--add-category="StrategyGame" \
			--dir %{buildroot}%{_datadir}/applications \
            %{buildroot}%{_datadir}/applications/*.desktop

%find_lang %{name}

# omit ggz.modules, to register at install, not build, time.
%__rm %{buildroot}%{_sysconfdir}/ggz.modules
# include .dsc files
%__mkdir_p %{buildroot}%{_datadir}/ggz
%__install -p -D -m644 data/civclient.dsc %{buildroot}%{_datadir}/ggz/civclient.dsc
%__install -p -D -m644 data/civclient.dsc %{buildroot}%{_datadir}/ggz/civserver.dsc 

#remove unneeded
# The Qt one will be useful as soon as the Qt client becomes more than a
# stub -- probably by 2.5.x
%__rm -f %{buildroot}%{_libdir}/*a
%__rm -f %{buildroot}%{_mandir}/man6/*ftwl*
%__rm -f %{buildroot}%{_mandir}/man6/*gtk3*
%__rm -f %{buildroot}%{_mandir}/man6/*qt*
%__rm -f %{buildroot}%{_mandir}/man6/*sdl*
%__rm -f %{buildroot}%{_mandir}/man6/*win32*
%__rm -f %{buildroot}%{_mandir}/man6/*xaw*

%clean
%__rm -rf %{buildroot}

%post client
%{_bindir}/ggz-config --install --force --modfile=%{_datadir}/ggz/civclient.dsc || :

%preun client
if [ $1 -eq 0 ]; then
   %{_bindir}/ggz-config --remove --modfile=%{_datadir}/ggz/civclient.dsc || :
fi

%post server
%{_bindir}/ggz-config --install --force --modfile=%{_datadir}/ggz/civserver.dsc || :

%preun server
if [ $1 -eq 0 ]; then
  %{_bindir}/ggz-config --remove --modfile=%{_datadir}/ggz/civserver.dsc || :
fi

%files -f %{name}.lang data
%doc AUTHORS doc/BUGS doc/HOWTOPLAY NEWS doc/README doc/README.AI doc/README.graphics doc/README.rulesets doc/README.sound doc/HACKING
%{_gamesdatadir}/%{name}

%files client
%{_gamesbindir}/freeciv-gtk2
%{_gamesbindir}/freeciv-manual
%{_gamesbindir}/freeciv-modpack
%{_mandir}/man6/freeciv-client.6*
%{_mandir}/man6/freeciv-gtk2.6*
%{_mandir}/man6/freeciv-modpack*
%{_datadir}/applications/freeciv.desktop
%{_datadir}/applications/freeciv-modpack.desktop
%{_datadir}/pixmaps/freeciv-client.png
%{_iconsdir}/hicolor/*/apps/freeciv-modpack.png
%{_iconsdir}/hicolor/*/apps/freeciv-client.png
%{_datadir}/ggz/civclient.dsc

%files server
%{_gamesbindir}/civserver.real
%{_gamesbindir}/freeciv-server
%{_mandir}/man6/freeciv-server.6*
%{_datadir}/applications/freeciv-server.desktop
%{_iconsdir}/hicolor/*/apps/freeciv-server.png
%{_datadir}/ggz/civserver.dsc
%_sysconfdir/freeciv


%changelog
* Fri Apr 13 2012 Götz Waschk <waschk@mandriva.org> 2.3.2-2mdv2012.0
+ Revision: 790488
- rebuild

  + Andrey Bondrov <abondrov@mandriva.org>
    - New version 2.3.2

* Mon Dec 05 2011 Alexander Khrukin <akhrukin@mandriva.org> 2.3.1-1
+ Revision: 737889
- version update fix
- version update

* Sun Oct 16 2011 Andrey Bondrov <abondrov@mandriva.org> 2.3.0-1
+ Revision: 704872
- New version 2.3.0

* Wed May 18 2011 Funda Wang <fwang@mandriva.org> 2.2.5-2
+ Revision: 675941
- add br

* Mon Mar 07 2011 Zombie Ryushu <ryushu@mandriva.org> 2.2.5-1
+ Revision: 642389
- upgrade to 2.2.5

* Tue Oct 12 2010 Funda Wang <fwang@mandriva.org> 2.2.3-3mdv2011.0
+ Revision: 585065
- obsoletes old packages

* Wed Sep 29 2010 Götz Waschk <waschk@mandriva.org> 2.2.3-2mdv2011.0
+ Revision: 582085
- make the data package noarch, not the client

* Tue Sep 28 2010 Samuel Verschelde <stormi@mandriva.org> 2.2.3-1mdv2011.0
+ Revision: 581899
- update to new version 2.2.3
- really fix source url
- fix URL

* Tue Aug 31 2010 Thierry Vignaud <tv@mandriva.org> 2.2.2-2mdv2011.0
+ Revision: 574907
- let the data subpackage be noarch

* Sun Aug 08 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.2-1mdv2011.0
+ Revision: 567753
- update to new version 2.2.2

* Thu Mar 18 2010 Emmanuel Andry <eandry@mandriva.org> 2.2.0-3mdv2010.1
+ Revision: 525050
- readd wrongly removed ggz game info scripts
- Requires (post and preun) ggz-client-libs

* Tue Mar 16 2010 Emmanuel Andry <eandry@mandriva.org> 2.2.0-2mdv2010.1
+ Revision: 522387
- drop ggz macros, they cause weird build issues. Use fixed paths instead

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - drop backwards compatible scriptlets for ancient releases
    - don't define name, version & release on top of spec
    - fix broken ggz macros resulting in files ending up in / (fixes #58123)

* Sat Feb 27 2010 Emmanuel Andry <eandry@mandriva.org> 2.2.0-1mdv2010.1
+ Revision: 512338
- New version 2.2.0
- use proper ggz components packaging

* Mon Feb 01 2010 Emmanuel Andry <eandry@mandriva.org> 2.1.11-1mdv2010.1
+ Revision: 499231
- New version 2.1.11

* Sat Nov 28 2009 Frederik Himpe <fhimpe@mandriva.org> 2.1.10-1mdv2010.1
+ Revision: 471003
- update to new version 2.1.10

* Sun May 24 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.9-1mdv2010.0
+ Revision: 379214
- new version

* Mon Mar 09 2009 Emmanuel Andry <eandry@mandriva.org> 2.1.8-4mdv2009.1
+ Revision: 353337
- fix locale path (#46043)

* Wed Feb 25 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.8-3mdv2009.1
+ Revision: 344752
- rebuild against new readline
- keep bash completion in its own package

* Sun Dec 14 2008 Zombie Ryushu <ryushu@mandriva.org> 2.1.8-1mdv2009.1
+ Revision: 314373
- New Version 2.1.8
- Version bump to 2.1.8

* Thu Aug 28 2008 Emmanuel Andry <eandry@mandriva.org> 2.1.6-1mdv2009.0
+ Revision: 277057
- New version

* Sun Jun 29 2008 Funda Wang <fwang@mandriva.org> 2.1.5-1mdv2009.0
+ Revision: 229944
- New version 2.1.5

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sat May 03 2008 Funda Wang <fwang@mandriva.org> 2.1.4-1mdv2009.0
+ Revision: 200636
- fix ggz-gtk-client devel package name

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - new version

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Fri Feb 01 2008 Funda Wang <fwang@mandriva.org> 2.1.3-1mdv2008.1
+ Revision: 161008
- New version 2.1.3

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Nov 28 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.1-1mdv2008.1
+ Revision: 113770
- update to new version 2.1.1

* Sun Nov 11 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.0-2mdv2008.1
+ Revision: 107952
- decompressed additional sources
- fix wrapper perms (fix bug#35451)

* Wed Nov 07 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.0-1mdv2008.1
+ Revision: 106825
- sanitize perms
- use upstream icons
- new version

* Mon Sep 17 2007 Emmanuel Andry <eandry@mandriva.org> 2.0.9-3mdv2008.0
+ Revision: 89330
- reintroduce configure2_5x
- drop duplicate category in desktop file
- set optimzation to -O1 to fix bug #33680

* Sat Sep 01 2007 Emmanuel Andry <eandry@mandriva.org> 2.0.9-2mdv2008.0
+ Revision: 77707
- drop old menu
- configure2_5x is no more

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Sun Feb 18 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.9-1mdv2007.0
+ Revision: 122382
- 2.0.9
- regenerate P0
- Import freeciv

* Wed Sep 20 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.8-5mdv2007.0
- rebuild

* Fri Aug 25 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.8-4mdv2007.0
- fix so that we use the icon we supply in the xdg menu (P2)

* Tue Aug 15 2006 Götz Waschk <waschk@mandriva.org> 2.0.8-3mdv2007.0
- fix buildrequires

* Mon Jul 31 2006 Emmanuel Andry <eandry@mandriva.org> 2.0.8-2mdv2007.0
- xdg menu

* Mon Mar 06 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.8-1mdk
- New release 2.0.8

* Mon Nov 07 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.7-1mdk
- New release 2.0.7

* Sat Oct 01 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.6-1mdk
- 2.0.6

* Tue Aug 09 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.4-2mdk
- fix problem with translations not being used (P0 from debian, fixes #15720)
- show in the caravan dialog how many shields remain to have a wonder built (P1 from debian)
- fix requires-on-release
- make client require server as it's required for single player games

* Fri Aug 05 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.4-1mdk
- New release 2.0.4

* Fri Aug 05 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.3-2mdk
- Rebuild

* Fri Jul 22 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.3-1mdk
- 2.0.3

* Fri Jul 08 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.2-1mdk
- 2.0.2

* Mon May 02 2005 Nicolas Chipaux <chipaux@mandriva.com> 2.0.1-1mdk
- 2.0.1

* Tue Apr 19 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.0.0-1mdk
- 2.0.0
- %%mkrel

* Thu Jan 20 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.14.2-2mdk
- rebuild for new readline

* Mon Nov 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.14.2-1mdk
- 1.14.2
- drop Packager tag

