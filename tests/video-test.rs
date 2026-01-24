use https_an::{Video, has_name::has_name};

#[test]
fn test_name_not_changed() {
    let typical_name = &"TypicalName";
    let vidio_with_typical_name = Video{name: typical_name.to_string()};

    assert_eq!(vidio_with_typical_name.name(), typical_name.to_string());
}