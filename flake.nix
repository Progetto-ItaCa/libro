{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
        tex = pkgs.texlive.combine {
          inherit
            (pkgs.texlive)
            scheme-basic
            collection-langcyrillic
            collection-basic
            collection-latex
            collection-fontsrecommended
            adjustbox
            alphalph
            babel-italian
            booktabs
            caption
            circuitikz
            cm-super
            collectbox
            cjk
            csquotes
            cyrillic
            datetime
            enumitem
            epigraph
            etoolbox
            fancyvrb
            fmtcount
            fontawesome
            hologo
            hypdoc
            hyphenat
            ifoddpage
            imakeidx
            infwarerr
            itnumpar
            jknapltx
            koma-script
            latexmk
            latexindent
            lh
            mathabx
            mathtools
            metafont
            microtype
            minted
            multirow
            nextpage
            pgf
            snapshot
            stmaryrd
            t2
            texfot
            tikz-cd
            todonotes
            turnstile
            ucs
            underscore
            upquote
            varwidth
            xcolor
            xkeyval
            xpatch
            xypic
            ;
        };
      in rec {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            tex
          ];
        };
        packages = {
          document = pkgs.stdenvNoCC.mkDerivation rec {
            name = "teoria-delle-categorie";
            src = self;
            buildInputs = [pkgs.coreutils tex];
            phases = ["unpackPhase" "buildPhase" "installPhase"];
            buildPhase = ''
              env \
                TEXMFVAR=$(pwd)/.texmf-var \
                TEXMFHOME=$(pwd)/.texmf-home  \
                TEXMFCACHE=$(pwd)/.texmf-cache \
                TEXMFCONFIG=$(pwd)/.texmf-config \
                SOURCE_DATE_EPOCH=${toString self.lastModified} \
              make main.pdf
            '';
            installPhase = ''
              mkdir -p $out
              cp main.pdf $out/
            '';
          };
        };
        defaultPackage = packages.document;
      }
    );
}
