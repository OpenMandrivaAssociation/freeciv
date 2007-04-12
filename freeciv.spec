%define	name	freeciv
%define version	2.0.9
%define rel	1
%define release %mkrel %{rel}

Name:		%{name}
Summary:	FREE CIVilization clone
Version:	%{version}
Release:	%{release}
Source0:	ftp://ftp.freeciv.org/freeciv/stable/%{name}-%{version}.tar.bz2
Source1:	%{name}.server.wrapper.bz2
Source2:	stdsounds2.tar.bz2
Source3:	%{name}.bash-completion.bz2
Source10:	%{name}-client.16.png
Source11:	%{name}-client.32.png
Source12:	%{name}-client.48.png
Source20:	%{name}-server.16.png
Source21:	%{name}-server.32.png
Source22:	%{name}-server.48.png
Patch0:		freeciv-2.0.9-configure_ac_localedir.patch
Patch1:		freeciv-1.14.1-caravan-show-shields.patch
Patch2:		freeciv-2.0.8-fix-icon.patch
License:	GPL
Group:		Games/Strategy
BuildRequires:	SDL_mixer-devel gtk+2-devel ncurses-devel readline-devel
BuildRequires:	desktop-file-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.freeciv.org/

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

%description    client
This is the graphical client for freeciv

%package        server
Group:          Games/Strategy
Summary:        FREE CIVilization clone - server
Provides:	%{name}
Obsoletes:	%{name}
Requires:	%{name}-data = %{version}

%description    server
This is the server for freeciv.

%prep
%setup -q
%patch0 -p1 -b .locale
%patch1 -p1 -b .caravan
%patch2 -p1 -b .icon
bzcat %{SOURCE3} > %{name}.bash-completion

%build
autoconf
%configure2_5x	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir} \
		--enable-client=gtk-2.0 
%make

%install
rm -rf %{buildroot}
%makeinstall_std localedir=%{_datadir}/locale

tar -jxf %{SOURCE2} -C %{buildroot}%{_gamesdatadir}/%{name}

# icons
install -m644 %{SOURCE10} -D %{buildroot}%{_miconsdir}/%{name}-client.png
install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/%{name}-client.png
install -m644 %{SOURCE12} -D %{buildroot}%{_liconsdir}/%{name}-client.png
install -m644 %{SOURCE20} -D %{buildroot}%{_miconsdir}/%{name}-server.png
install -m644 %{SOURCE21} -D %{buildroot}%{_iconsdir}/%{name}-server.png
install -m644 %{SOURCE22} -D %{buildroot}%{_liconsdir}/%{name}-server.png

# wrapper
mv %{buildroot}%{_gamesbindir}/civserver %{buildroot}%{_gamesbindir}/civserver.real
bzcat %{SOURCE1} > %{buildroot}%{_gamesbindir}/civserver

# menu entry
mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name}-client <<EOF
?package(%{name}-client):\
	needs="x11"\
	section="More Applications/Games/Strategy"\
	title="Freeciv client"\
	longtitle="The Free Civilization Clone"\
	command="%{_gamesbindir}/civclient"\
	icon="%{name}-client.png"\
	xdg="true"
EOF

desktop-file-install	--vendor="" \
			--remove-category="Application" \
			--remove-category="GNOME" \
			--remove-category="Strategy" \
			--add-category="GTK" \
			--add-category="Game;StrategyGame" \
			--add-category="X-MandrivaLinux-MoreApplications-Games-Strategy" \
			--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

cat > %{buildroot}%{_menudir}/%{name}-server <<EOF
?package(%{name}-server):\
	needs="text"\
	section="More Applications/Games/Strategy"\
	title="Freeciv server"\
	longtitle="The Free Civilization Clone (server)"\
	command="%{_gamesbindir}/civserver"\
	icon="%{name}-server.png"\
	xdg="true"
EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-server.desktop << EOF
[Desktop Entry]
Name=%{name}-server
Comment=The Free Civilization Clone (server)
Exec=%{_gamesbindir}/civserver
Icon=%{name}-server
Terminal=true
Type=Application
Categories=ConsoleOnly;Game;StrategyGame;X-MandrivaLinux-MoreApplications-Games-Strategy;
Encoding=UTF-8
EOF

%find_lang %{name}

install -m644 %{name}.bash-completion -D %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%post client
%update_menus

%postun client
%clean_menus

%post server
%update_menus

%postun server
%clean_menus

%clean
rm -rf %{buildroot}

%files -f %{name}.lang data
%defattr(644,root,root,0755)
%doc AUTHORS doc/BUGS doc/HOWTOPLAY NEWS doc/README doc/README.AI doc/README.graphics doc/README.rulesets doc/README.sound doc/HACKING
%defattr(644,root,games,0755)
%{_gamesdatadir}/%{name}
%config(noreplace) %{_sysconfdir}/bash_completion.d/%{name}

%files client
%defattr(755,root,games,0755)
%{_gamesbindir}/civclient
%{_gamesbindir}/civmanual
%defattr(644,root,root,0755)
%{_menudir}/%{name}-client
%{_iconsdir}/%{name}-client.png
%{_miconsdir}/%{name}-client.png
%{_liconsdir}/%{name}-client.png
%{_mandir}/man6/civclient.6*
%{_datadir}/applications/freeciv.desktop

%files server
%defattr(755,root,games,0755)
%{_gamesbindir}/civserver*
%defattr(644,root,root,0755)
%{_menudir}/%{name}-server
%{_iconsdir}/%{name}-server.png
%{_miconsdir}/%{name}-server.png
%{_liconsdir}/%{name}-server.png
%{_mandir}/man6/civserver.6*
%{_datadir}/applications/mandriva-%{name}-server.desktop


