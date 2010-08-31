Name:		freeciv
Version:	2.2.2
Release:	%mkrel 2
Summary:	CIVilization clone
License:	GPLv2+
Group:		Games/Strategy
URL:		http://www.freeciv.org/
Source0:	http://prdownloads.sourceforge.net/freeciv/%{name}-%{version}.tar.bz2
Source1:	%{name}.server.wrapper
Source2:	stdsounds2.tar.bz2
BuildRequires:	SDL_mixer-devel
BuildRequires:	gtk+2-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	desktop-file-utils
BuildRequires:	ggz-gtk-client-devel
Requires(post): ggz-client-libs
Requires(preun): ggz-client-libs
BuildRoot:	%{_tmppath}/%{name}-%{version}

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

%description	data
Freeciv is a multiplayer strategy game, released under the GNU General
Public License. It is generally comparable with Civilization II(r),
published by Microprose(r).

Default configuration uses the Civilization II(r) style Isometric view. If
you prefer classic Civilization(r) 2-d view, invoke the client with
"civclient --tiles trident".

%package        client
Group:          Games/Strategy
Summary:        FREE CIVilization clone - client
Provides:	%{name}
Obsoletes:	%{name}
Requires:	%{name}-data = %{version} %{name}-server = %{version}
Requires(post):	ggz-client-libs
Requires(preun): ggz-client-libs 
BuildArch: noarch

%description    client
This is the graphical client for freeciv

%package        server
Group:          Games/Strategy
Summary:        FREE CIVilization clone - server
Provides:	%{name}
Obsoletes:	%{name}
Requires:	%{name}-data = %{version}
Requires(post):	ggz-client-libs
Requires(preun): ggz-client-libs 

%description    server
This is the server for freeciv.

%prep
%setup -q

%build
#locales are not in %{_gamesdatadir}
export localedir=%{_datadir}/locale

%configure2_5x \
    --bindir=%{_gamesbindir} \
    --datadir=%{_gamesdatadir} \
    --enable-client=gtk-2.0 
%make

%install
rm -rf %{buildroot}
%makeinstall_std localedir=%{_datadir}/locale

tar -jxf %{SOURCE2} -C %{buildroot}%{_gamesdatadir}/%{name}

# wrapper
mv %{buildroot}%{_gamesbindir}/freeciv-server %{buildroot}%{_gamesbindir}/civserver.real
install -m 755 %{SOURCE1} %{buildroot}%{_gamesbindir}/freeciv-server

# fix icons locations
mv %{buildroot}%{_gamesdatadir}/icons %{buildroot}%{_datadir}/icons

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
rm %{buildroot}%{_sysconfdir}/ggz.modules
# include .dsc files
mkdir -p %{buildroot}%{_datadir}/ggz
install -p -D -m644 data/civclient.dsc %{buildroot}%{_datadir}/ggz/civclient.dsc
install -p -D -m644 data/civclient.dsc %{buildroot}%{_datadir}/ggz/civserver.dsc 

#remove unneeded
rm -f %{buildroot}%{_libdir}/*a
rm -f %{buildroot}%{_mandir}/man6/*ftwl*
rm -f %{buildroot}%{_mandir}/man6/*sdl*
rm -f %{buildroot}%{_mandir}/man6/*win32*
rm -f %{buildroot}%{_mandir}/man6/*xaw*

%clean
rm -rf %{buildroot}

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
%defattr(-,root,root)
%doc AUTHORS doc/BUGS doc/HOWTOPLAY NEWS doc/README doc/README.AI doc/README.graphics doc/README.rulesets doc/README.sound doc/HACKING
%{_gamesdatadir}/%{name}

%files client
%defattr(-,root,root)
%{_gamesbindir}/freeciv-gtk2
%{_gamesbindir}/civmanual
%{_mandir}/man6/freeciv-client.6*
%{_mandir}/man6/freeciv-gtk2.6*
%{_datadir}/applications/freeciv.desktop
%{_datadir}/pixmaps/freeciv-client.png
%{_iconsdir}/hicolor/*/apps/freeciv-client.png
%{_datadir}/ggz/civclient.dsc

%files server
%defattr(-,root,root)
%{_gamesbindir}/civserver.real
%{_gamesbindir}/freeciv-server
%{_mandir}/man6/freeciv-server.6*
%{_datadir}/applications/freeciv-server.desktop
%{_iconsdir}/hicolor/*/apps/freeciv-server.png
%{_datadir}/ggz/civserver.dsc
