use core::fmt;
use std::{fs, path::Path};

use clap::ValueEnum;

use crate::{
    document::{text_to_html, SupportedMarkup},
    project::BartProject,
};

#[derive(Debug, ValueEnum, Clone, Copy, PartialEq, Eq)]
pub enum BuildTargets {
    Html,
    Word,
    Pdf,
}

impl fmt::Display for BuildTargets {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            BuildTargets::Html => write!(f, "html"),
            BuildTargets::Word => write!(f, "word"),
            BuildTargets::Pdf => write!(f, "pdf"),
        }
    }
}

pub struct Builder {
    pub project: BartProject,
    pub target: BuildTargets,
}

impl Builder {
    pub fn build(&self) {
        let out_file_name = &self.project.name.clone().replace(" ", "-");
        let html = self.to_html();
        match &self.target {
            BuildTargets::Html => {
                let out_path = Path::new(&out_file_name);
                fs::write(out_path.with_extension("html"), html.concat())
                    .expect("Error writing HTML")
            }
            BuildTargets::Word => todo!(),
            BuildTargets::Pdf => todo!(),
        }
    }

    /// All formats at least pitstop in HTML
    fn to_html(&self) -> Vec<String> {
        let mut html_strings = Vec::new();
        for doc in self.project.documents.iter() {
            let html = match doc.get_markup_language() {
                SupportedMarkup::Markdown => markdown::to_html(&doc.read()),
                SupportedMarkup::Text => text_to_html(&doc.read()),
                _ => panic!("Not implemented."),
            };
            html_strings.push(html)
        }
        html_strings
    }
}
