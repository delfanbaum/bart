use core::fmt;
use std::{fmt::format, fs, path::Path};

use clap::ValueEnum;

use crate::{
    document::{Document, SupportedMarkup},
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
    project: Option<BartProject>,
    docs: Vec<Document>,
    target: BuildTargets,
}

impl Builder {
    pub fn build(&self) {
        let out_file_name = match &self.project {
            Some(project) => project.name.clone(),
            None => self.docs[0].path.to_str().unwrap().to_owned(),
        };

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
        for doc in self.docs.iter() {
            let html = match doc.get_markup_language() {
                SupportedMarkup::Markdown => markdown::to_html(&doc.read()),
                SupportedMarkup::Text => text_to_html(&doc.read()),
            };
            html_strings.push(html)
        }
        html_strings
    }
}

// this needs testing!
fn text_to_html(value: &str) -> String {
    println!("{}", value);
    let paras: Vec<_> = value.split("\n\n").collect();
    let html: String = paras.into_iter().map(|p| format!("<p>{p}</p>")).collect();
    println!("{}", html);
    html
}
