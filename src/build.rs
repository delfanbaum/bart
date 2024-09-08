use core::fmt;
use std::{fs, path::Path};

use clap::ValueEnum;
use markdown;
use regex::Regex;
use scraper::{Html, Selector};

use crate::{project::BartProject, project::SupportedMarkup};

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
        let html = self.project_to_html();
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
    fn project_to_html(&self) -> Vec<String> {
        let mut html_strings = Vec::new();
        for doc in self.project.documents.iter() {
            let html = to_html(&doc.read(), &self.project.markup_language);
            html_strings.push(html)
        }
        html_strings
    }
}

/// Generic converter function
pub fn to_html(text: &str, markup: &SupportedMarkup) -> String {
    match markup {
        SupportedMarkup::Asciidoc => todo!(),
        SupportedMarkup::SimplifiedAsciidoc => todo!(),
        SupportedMarkup::Markdown => markdown::to_html(text),
        SupportedMarkup::Text => text_to_html(text),
    }
}

// A very "dumb" implementation, but really folks should use a markup language anyway.
pub fn text_to_html(value: &str) -> String {
    println!("{}", value);
    let paras: Vec<_> = value.split("\n\n").collect();
    let html: String = paras
        .into_iter()
        .fold(String::new(), |acc, p| acc + &format!("<p>{p}</p>"));
    html
}

pub fn count_words(html: &str) -> usize {
    let re = Regex::new(r"(\w+)").unwrap();
    let html = Html::parse_fragment(html);
    let selector = Selector::parse("p").unwrap();
    let mut count = 0;
    for e in html.select(&selector) {
        let text = e.text();
        count += text.fold(0, |tcount, t| tcount + re.captures_iter(t).count());
        println!("{:?}", count);
    }
    count
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn text_to_html_makes_ps() {
        let text = "This should be one paragraph

This, another.";
        assert_eq!(
            text_to_html(text),
            "<p>This should be one paragraph</p><p>This, another.</p>"
        )
    }

    #[test]
    fn test_count_words() {
        // Note, it must be a markdown file so we can ensure we're not counting markup, etc.
        // so the issue is that ", Three" counts as two. So we need to only count words

        let html = to_html("--- \n One, _Two_, Three", &SupportedMarkup::Markdown);
        assert_eq!(count_words(&html), 3)
    }
}
