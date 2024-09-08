use core::panic;
use std::{fs, path::PathBuf};

use regex::Regex;
use scraper::{Html, Selector};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub enum SupportedMarkup {
    Asciidoc,
    Markdown,
    Text,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Document {
    pub path: PathBuf,
    pub description: String,
    pub word_count: usize,
}

impl Default for Document {
    fn default() -> Self {
        Document {
            path: PathBuf::new(),
            description: String::new(),
            word_count: 0,
        }
    }
}

impl Document {
    pub fn get_markup_language(&self) -> SupportedMarkup {
        match self.path.extension().unwrap().to_str().unwrap() {
            "adoc" | "asciidoc" => SupportedMarkup::Asciidoc,
            "md" | "markdown" => SupportedMarkup::Markdown,
            "txt" => SupportedMarkup::Text,
            _ => panic!("Filetype not supported"),
        }
    }

    pub fn read(&self) -> String {
        fs::read_to_string(&self.path).expect("Error reading file {self.path}")
    }

    pub fn to_html(&self) -> String {
        match self.get_markup_language() {
            SupportedMarkup::Asciidoc => panic!("Not implemented yet!"),
            SupportedMarkup::Markdown => markdown::to_html(&self.read()),
            SupportedMarkup::Text => text_to_html(&self.read()),
        }
    }

    /// Counts the number of words (in the body <p> text), updates self, and returns for
    /// consumption elsewhere.
    pub fn count(&mut self) -> usize {
        let re = Regex::new(r"(\w+)").unwrap();
        let html = Html::parse_fragment(&self.to_html());
        let selector = Selector::parse("p").unwrap();
        let mut count = 0;
        for e in html.select(&selector) {
            let text = e.text();
            count += text.fold(0, |tcount, t| tcount + re.captures_iter(t).count());
            println!("{:?}", count);
        }
        self.word_count = count;
        count
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

#[cfg(test)]
mod tests {
    use std::fs;
    use tempfile::TempPath;

    use super::*;

    #[test]
    fn test_count() {
        // Note, it must be a markdown file so we can ensure we're not counting markup, etc.
        let file = TempPath::from_path("test.md");
        // so the issue is that ", Three" counts as two. So we need to only count words
        fs::write(&file, "--- \n One, _Two_, Three".to_string()).expect("Error setting up test.");

        let mut doc = Document {
            path: file.to_path_buf(),
            ..Default::default()
        };
        assert_eq!(*&doc.count(), 3)
    }

    #[test]
    fn text_to_html_makes_ps() {
        let text = "This should be one paragraph

This, another.";
        assert_eq!(
            text_to_html(text),
            "<p>This should be one paragraph</p><p>This, another.</p>"
        )
    }
}
