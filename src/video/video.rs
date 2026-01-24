use crate::has_name::HasName;

pub struct Video { 
    pub name: String
}

impl HasName for Video {
    fn new(name: String) -> Self {
        Video {name}
    }

    fn name(&self) -> &str {
        &self.name
    }
}